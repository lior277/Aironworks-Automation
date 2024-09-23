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
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.page_objects.employee_reports_page import EmployeeReportsPage
from src.page_objects.entity.content_library_entity import ContentLibraryEntity
from src.page_objects.groups.groups_page import GroupsPage
from src.page_objects.login_page import SignInPage
from src.page_objects.outlook_page import OutlookPage
from src.page_objects.scenarios_page import ScenariosPage
from src.utils.log import Log
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
    Log.info(f'Browser version = {browser.version}')
    context = browser.new_context(
        viewport={'width': 1440, 'height': 900},
        permissions=['clipboard-read', 'clipboard-write'],
    )
    context.set_default_timeout(timeout=120 * 1000)
    expect.set_options(timeout=10_000)
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


@pytest.fixture(scope='function')
def outlook_page(playwright_config) -> OutlookPage:
    page: Page = playwright_config[1].new_page()

    outlook_page = OutlookPage(page)
    outlook_page.login()

    return outlook_page


@pytest.fixture(scope='function')
def sign_in_page(playwright_config) -> SignInPage:
    # page.set_viewport_size({"width": 640, "height": 480})
    # we want to use the already existing context
    page: Page = playwright_config[1].new_page()
    return SignInPage(page)


@pytest.fixture(scope='function')
def dashboard_page(sign_in_page: SignInPage, user: UserModel) -> DashboardPage:
    refresh_token = f'{user.email}_refresh_token'
    session = f'{user.email}_session'
    token = f'{user.email}_token'
    if os.getenv(refresh_token):
        sign_in_page.page.set_extra_http_headers(
            {
                'Cookie': f'refresh_token={os.environ[refresh_token]}; session={os.environ[session]};token={os.environ[token]}'
            }
        )
        response = sign_in_page.navigate(admin=user.is_admin)
        sign_in_page.wait_for_page_loaded(user.is_admin)
        assert response.ok, f'{response.status_text=}'

        def wait_for_cookies():
            return sign_in_page.page.context.storage_state()['cookies']

        assert wait_for(
            wait_for_cookies, timeout=15
        ), f'cookies were not applied {wait_for_cookies=}'
        Log.info(f"{sign_in_page.page.context.storage_state()["cookies"]=}")

    else:
        sign_in_page.navigate(admin=user.is_admin)
        sign_in_page.submit_sign_in_form(user)
        cookies = sign_in_page.page.context.cookies()
        os.environ[refresh_token] = cookies[0]['value']
        os.environ[session] = cookies[1]['value']
        os.environ[token] = cookies[2]['value']
    return DashboardPage(sign_in_page.page)


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
def customers_page(dashboard_page: DashboardPage) -> CustomersPage:
    return CustomersPage(dashboard_page.page)


@pytest.fixture
def campaign_details_page(dashboard_page: DashboardPage) -> CampaignDetailsPage:
    return CampaignDetailsPage(dashboard_page.page).open(
        campaign_id=AppConfigs.SAMPLE_CAMPAIGN
    )


@pytest.fixture
def groups_page(dashboard_page: DashboardPage) -> GroupsPage:
    return dashboard_page.navigation_bar.navigate_groups_page()
