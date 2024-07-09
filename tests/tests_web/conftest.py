import os
import tempfile

import allure
import pytest
from playwright.sync_api import Browser, Page

from src.models.auth.user_model import UserModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.page_objects.campaigns_page import CampaignsPage
from src.page_objects.content_library_page import ContentLibraryPage
from src.page_objects.customers_page import CustomersPage
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.education_campaign.education_campaign_details_page import EducationCampaignDetailsPage
from src.page_objects.education_campaign.education_campaign_page import EducationCampaignPage
from src.page_objects.employee_reports_page import EmployeeReportsPage
from src.page_objects.login_page import SignInPage
from src.page_objects.scenarios_page import ScenariosPage
from src.utils.log import Log
from src.utils.waiter import wait_for


@pytest.fixture(scope="function")
def playwright_config(request, launch_browser, browser_type):
    # with sync_playwright() as p:
    args = None
    if browser_type.name == "chromium":
        args = ["--single-process"]
    browser: Browser = launch_browser(args=args)
    Log.info(f"Browser version = {browser.version}")
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        permissions=["clipboard-read", "clipboard-write"],
    )
    context.set_default_timeout(timeout=120 * 1000)

    context.tracing.start(
        name=request.node.name, snapshots=True, screenshots=True, sources=True
    )

    yield browser, context

    # If request.node is missing rep_call, then some error happened during execution
    # that prevented teardown, but should still be counted as a failure
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else True

    traceout = tempfile.mktemp(prefix="trace")

    if failed:
        context.tracing.stop(path=traceout)
        allure.attach.file(traceout, "trace.zip", "zip")
        for page in context.pages:
            allure.attach(page.screenshot(), name=f"{page.title()}.png",
                          attachment_type=allure.attachment_type.PNG)
    else:
        context.tracing.stop()

    context.close()
    browser.close()


@pytest.fixture(scope="function")
def sign_in_page(playwright_config) -> SignInPage:
    # page.set_viewport_size({"width": 640, "height": 480})
    # we want to use the already existing context
    page: Page = playwright_config[1].new_page()
    return SignInPage(page)


@pytest.fixture(scope="function")
def dashboard_page(sign_in_page: SignInPage, user: UserModel) -> DashboardPage:
    remember_token = f"{user.email}_remember_token"
    session = f"{user.email}_session"
    if os.getenv(remember_token):
        sign_in_page.page.context.set_extra_http_headers(
            {"Cookie": f"remember_token={os.environ[remember_token]}; session={os.environ[session]}"})
        sign_in_page.navigate(admin=user.is_admin)

        def wait_for_cookies():
            return sign_in_page.page.context.storage_state()['cookies']

        wait_for(wait_for_cookies, timeout=10)

    else:
        sign_in_page.navigate(admin=user.is_admin)
        sign_in_page.submit_sign_in_form(user)
        cookies = sign_in_page.page.context.cookies()
        os.environ[remember_token] = cookies[0]['value']
        os.environ[session] = cookies[1]['value']
    return DashboardPage(sign_in_page.page)


@pytest.fixture(scope="function")
def education_campaign_page(dashboard_page: DashboardPage) -> EducationCampaignPage:
    return dashboard_page.navigation_bar.navigate_education_campaigns_page()


@pytest.fixture(scope="function")
def education_campaign_detail_page(education_campaign_page,
                                   education_campaign: EducationCampaignDetailsModel) -> EducationCampaignDetailsPage:
    return education_campaign_page.open_campaign_details(education_campaign.title)


@pytest.fixture(scope="function")
def content_library_page(dashboard_page: DashboardPage) -> ContentLibraryPage:
    return dashboard_page.navigation_bar.navigate_content_library()


@pytest.fixture(scope="function")
def employee_reports_page(dashboard_page: DashboardPage) -> EmployeeReportsPage:
    return dashboard_page.navigation_bar.navigate_employee_reports()


@pytest.fixture(scope="function")
def scenarios_page(dashboard_page: DashboardPage) -> ScenariosPage:
    return dashboard_page.navigation_bar.navigate_scenarios()


@pytest.fixture(scope="function")
def campaigns_page(dashboard_page: DashboardPage) -> CampaignsPage:
    return dashboard_page.navigation_bar.navigate_campaigns()


@pytest.fixture(scope="function")
def customers_page(dashboard_page: DashboardPage, user: UserModel) -> CustomersPage:
    return CustomersPage(dashboard_page.page, user)
