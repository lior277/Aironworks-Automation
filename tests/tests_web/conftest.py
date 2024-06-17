import tempfile

import allure
import pytest
from playwright.sync_api import Browser, Page

from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage
from src.utils.log import Log


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
    # return SignInPage(page)


@pytest.fixture(scope="function")
def dashboard_page(sign_in_page: SignInPage) -> DashboardPage:
    return DashboardPage(sign_in_page.page)
