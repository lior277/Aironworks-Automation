import pytest
from playwright.sync_api import Browser

from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage
from src.utils.log import Log


@pytest.fixture(scope="function")
def playwright_config(browser: Browser):
    Log.info(f"Browser version = {browser.version}")
    context = browser.new_context()

    yield browser, context
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def sign_in_page(playwright_config) -> SignInPage:
    # page.set_viewport_size({"width": 640, "height": 480})
    page = playwright_config[0].new_page(screen={"width": 640, "height": 480})
    return SignInPage(page)
    # return SignInPage(page)


@pytest.fixture(scope="function")
def dashboard_page(sign_in_page: SignInPage) -> DashboardPage:
    return DashboardPage(sign_in_page.page)
