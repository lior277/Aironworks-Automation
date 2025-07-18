import os
import tempfile

import allure
import pytest
from playwright.sync_api import Browser, Page, expect

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.page_objects.campaign_details_page import CampaignDetailsPage
from src.page_objects.campaigns_page import CampaignsPage
from src.page_objects.content_library.add_content_page import AddContentPage
from src.page_objects.content_library.content_library_page import ContentLibraryPage
from src.page_objects.customers_page import CustomersPage
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.education_campaign.education_campaign_details_page import (
    EducationCampaignDetailsPage,
)
from src.page_objects.education_campaign.education_campaign_page import (
    EducationCampaignPage,
)
from src.page_objects.email_filter.email_filter_settings_page import (
    EmailFilterSettingsPage,
)
from src.page_objects.email_filter.email_statistics_page import EmailStatisticsPage
from src.page_objects.email_filter.received_emails_page import ReceivedEmailsPage
from src.page_objects.employee_dashboard.employee_dashboard_page import (
    EmployeeDashboardPage,
)
from src.page_objects.employee_directory.add_admin_page import AddAdminPage
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.page_objects.employee_reports_page import EmployeeReportsPage
from src.page_objects.entity.content_library_entity import ContentLibraryEntity
from src.page_objects.groups.groups_page import GroupsPage
from src.page_objects.login_page import SignInPage
from src.page_objects.operations.operations_list_page import OperationsListPage
from src.page_objects.outlook_page import OutlookPage
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_configuration_page import (
    PhishDetectAISettingsConfiguration,
)
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_general_page import (
    PhishDetectAISettingsGeneral,
)
from src.page_objects.scenarios_page import ScenariosPage
from src.page_objects.training_settings.email_sending_page import EmailSendingPage
from src.page_objects.training_settings.group_settings_page import GroupSettingsPage
from src.utils.log import Log
from src.utils.sendgrid import SendGrid
from src.utils.waiter import wait_for


def safe_title(page: Page) -> str:
    try:
        return page.title()
    except Exception as e:
        Log.warning(f'Failed to get page title: {e}')
        return 'unknown'


@pytest.fixture(scope='function')
def playwright_config(request, launch_browser, browser_type):
    # with sync_playwright() as p:
    args = None
    if browser_type.name == 'chromium':
        args = ['--single-process']
    browser: Browser = launch_browser(args=args)
    if not os.getenv('BROWSER_NAME'):
        os.environ['BROWSER_NAME'] = browser.browser_type.name
        os.environ['BROWSER_VERSION'] = browser.version
    Log.info(f'Browser version = {browser.version}')
    context = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        permissions=['clipboard-read', 'clipboard-write'],
    )
    context.set_default_timeout(timeout=120 * 1000)
    expect.set_options(timeout=20_000)
    context.tracing.start(
        name=request.node.name, snapshots=True, screenshots=True, sources=True
    )

    yield browser, context

    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, 'rep_call') else True

    traceout = tempfile.mktemp(prefix='trace')

    if failed:
        context.tracing.stop(path=traceout)
        allure.attach.file(traceout, 'trace.zip', 'zip')
        for page in context.pages:
            allure.attach(
                page.screenshot(),
                name=f'{safe_title(page)}.png',
                attachment_type=allure.attachment_type.PNG,
            )
    else:
        context.tracing.stop()

    context.close()
    browser.close()


def send_random_email(from_email: str):
    sendgrid = SendGrid(AppConfigs.SENDGRID_API_KEY)
    subject = sendgrid.send_random_mail(from_email)
    return subject


@pytest.fixture(scope='function')
def outlook_page(playwright_config) -> OutlookPage:
    page: Page = playwright_config[1].new_page()
    subject = send_random_email(AppConfigs.MSLIVE_USER)
    print(f'Subject: {subject}')
    outlook_page = OutlookPage(page)
    outlook_page.go_to_outlook()
    outlook_page.login()
    outlook_page.navigate_to_inbox()
    outlook_page.goto_message(subject)
    return outlook_page


@pytest.fixture(scope='function')
def outlook_page_shared(playwright_config) -> OutlookPage:
    page: Page = playwright_config[1].new_page()
    subject = send_random_email(AppConfigs.MSLIVE_SHARED_USER)
    outlook_page = OutlookPage(page)
    outlook_page.go_to_outlook()
    outlook_page.login()
    outlook_page.navigate_to_shared_inbox()
    outlook_page.goto_message(subject)
    return outlook_page


@pytest.fixture(scope='function')
def sign_in_page(playwright_config) -> SignInPage:
    # page.set_viewport_size({"width": 640, "height": 480})
    # we want to use the already existing context
    page: Page = playwright_config[1].new_page()
    return SignInPage(page)


def get_cookie_value(cookies, name):
    for cookie in cookies:
        if cookie['name'] == name:
            return cookie['value']
    raise ValueError(f'Cookie with name {name} not found')


@pytest.fixture(scope='function')
def dashboard_page(sign_in_page: SignInPage, user: UserModel) -> DashboardPage:
    refresh_token = f'{user.email}_refresh_token'
    token = f'{user.email}_token'
    if os.getenv(refresh_token):
        url = AppConfigs.BASE_URL
        if user.is_admin:
            url = AppConfigs.ADMIN_BASE_URL
        Log.info(f'{url=}')
        sign_in_page.page.context.add_cookies(
            [
                {
                    'name': 'refresh_token',
                    'value': os.environ[refresh_token],
                    'url': url,
                    'secure': True,
                    'httpOnly': True,
                },
                {
                    'name': 'token',
                    'value': os.environ[token],
                    'url': url,
                    'secure': True,
                    'httpOnly': True,
                },
            ]
        )
        response = sign_in_page.navigate(admin=user.is_admin)
        sign_in_page.wait_for_page_loaded(user.is_admin)
        assert response.ok, f'{response.status_text=}'

        def wait_for_cookies():
            return sign_in_page.page.context.storage_state()['cookies']

        assert wait_for(wait_for_cookies, timeout=15), (
            f'cookies were not applied {wait_for_cookies=}'
        )
        Log.info(f'{sign_in_page.page.context.storage_state()["cookies"]=}')

    else:
        sign_in_page.navigate(admin=user.is_admin)
        sign_in_page.submit_sign_in_form(user)
        cookies = sign_in_page.page.context.cookies()
        Log.info(f'{cookies=}')
        os.environ[refresh_token] = get_cookie_value(cookies, 'refresh_token')
        os.environ[token] = get_cookie_value(cookies, 'token')
    return DashboardPage(sign_in_page.page)


@pytest.fixture(scope='function')
def employee_dashboard_page(
    sign_in_page: SignInPage, user: UserModel
) -> EmployeeDashboardPage:
    sign_in_page.navigate_to_employee_sign_in_page()
    with sign_in_page.page.expect_popup() as popup_info:
        sign_in_page.login_with_microsoft()
    outlook_page = OutlookPage(popup_info.value)
    outlook_page.login()
    return EmployeeDashboardPage(sign_in_page.page)


@pytest.fixture(scope='function')
def education_campaign_page(dashboard_page: DashboardPage) -> EducationCampaignPage:
    return dashboard_page.navigation_bar.navigate_education_campaigns_page()


@pytest.fixture(scope='function')
def education_campaign_detail_page(
    education_campaign_page, education_campaign: EducationCampaignDetailsModel
) -> EducationCampaignDetailsPage:
    return education_campaign_page.open_campaign_details(education_campaign.title)


@pytest.fixture(scope='function')
def content_library_page(dashboard_page: DashboardPage) -> ContentLibraryPage:
    return dashboard_page.navigation_bar.navigate_content_library()


@pytest.fixture(scope='function')
def add_content_page(
    content_library_page: ContentLibraryPage, education_content: ContentLibraryEntity
) -> AddContentPage:
    return content_library_page.open_add_content_page(education_content.content_type)


@pytest.fixture(scope='function')
def employee_reports_page(dashboard_page: DashboardPage) -> EmployeeReportsPage:
    return dashboard_page.navigation_bar.navigate_employee_reports()


@pytest.fixture(scope='function')
def scenarios_page(dashboard_page: DashboardPage) -> ScenariosPage:
    return dashboard_page.navigation_bar.navigate_scenarios()


@pytest.fixture(scope='function')
def campaigns_page(dashboard_page: DashboardPage) -> CampaignsPage:
    return dashboard_page.navigation_bar.navigate_campaigns()


@pytest.fixture(scope='function')
def employee_directory_page(dashboard_page: DashboardPage) -> EmployeeDirectoryPage:
    return dashboard_page.navigation_bar.navigate_employee_directory()


@pytest.fixture(scope='function')
def add_admin_page(employee_directory_page: EmployeeDirectoryPage) -> AddAdminPage:
    return employee_directory_page.go_to_add_admin_page()


@pytest.fixture(scope='function')
def customers_page(dashboard_page: DashboardPage) -> CustomersPage:
    return CustomersPage(dashboard_page.page)


@pytest.fixture
def campaign_details_page(dashboard_page: DashboardPage) -> CampaignDetailsPage:
    return CampaignDetailsPage(dashboard_page.page).open(
        campaign_id=AppConfigs.SAMPLE_CAMPAIGN
    )


@pytest.fixture
def first_campaign_details_page(dashboard_page: DashboardPage) -> CampaignDetailsPage:
    campaigns_page = dashboard_page.navigation_bar.navigate_campaigns()
    return campaigns_page.click_first_ongoing_campaign()


@pytest.fixture
def groups_page(dashboard_page: DashboardPage) -> GroupsPage:
    return dashboard_page.navigation_bar.navigate_groups_page()


@pytest.fixture
def phish_detect_ai_settings_general_page(
    dashboard_page: DashboardPage,
) -> PhishDetectAISettingsGeneral:
    return (
        dashboard_page.navigation_bar.navigate_phish_detect_ai_settings_general_page()
    )


@pytest.fixture
def phish_detect_ai_settings_configuration_page(
    dashboard_page: DashboardPage,
) -> PhishDetectAISettingsConfiguration:
    return dashboard_page.navigation_bar.navigate_phish_detect_ai_settings_ui_page()


@pytest.fixture
def email_statistics_page(dashboard_page: DashboardPage) -> EmailStatisticsPage:
    return dashboard_page.navigation_bar.navigate_email_statistics_page()


@pytest.fixture
def email_filter_settings_page(
    dashboard_page: DashboardPage,
) -> EmailFilterSettingsPage:
    return dashboard_page.navigation_bar.navigate_email_filter_settings_page()


@pytest.fixture
def received_emails_page(dashboard_page: DashboardPage) -> ReceivedEmailsPage:
    return dashboard_page.navigation_bar.navigate_received_emails_page()


@pytest.fixture
def training_settings_email_sending_page(
    dashboard_page: DashboardPage,
) -> EmailSendingPage:
    return dashboard_page.navigation_bar.navigate_training_settings_email_sending_page()


@pytest.fixture
def operations_list_page(dashboard_page: DashboardPage) -> OperationsListPage:
    return dashboard_page.navigation_bar.navigate_operation_list_page()


@pytest.fixture
def training_settings_group_settings_page(
    dashboard_page: DashboardPage,
) -> GroupSettingsPage:
    return (
        dashboard_page.navigation_bar.navigate_training_settings_group_settings_page()
    )


@pytest.fixture(scope='function')
def is_staging_env():
    if AppConfigs.ENV != 'staging':
        pytest.skip('Attachment not available')
