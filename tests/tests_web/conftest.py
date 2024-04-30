import pytest
from playwright.sync_api import Browser, Page

from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage
from src.utils.log import Log
import tempfile
import allure


@pytest.fixture(scope="function")
def playwright_config(browser: Browser):
    Log.info(f"Browser version = {browser.version}")
    context = browser.new_context(screen={"width": 640, "height": 480})

    context.tracing.start(snapshots=True, screenshots=True, sources=True)

    yield browser, context

    traceout = tempfile.mktemp(prefix="trace")

    context.tracing.stop(path=traceout)

    allure.attach.file(traceout, "trace.zip", "zip")

    context.close()
    browser.close()


@pytest.fixture(scope="function")
def sign_in_page(playwright_config) -> SignInPage:
    # page.set_viewport_size({"width": 640, "height": 480})
    # we want to use the already existing context
    page: Page = playwright_config[1].new_page()
    return SignInPage(page)
    # return SignInPage(page)


@pytest.fixture(scope="function")
def dashboard_page(sign_in_page: SignInPage) -> DashboardPage:
    return DashboardPage(sign_in_page.page)
