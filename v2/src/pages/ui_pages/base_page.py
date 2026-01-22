"""Base page with optional API context."""

from playwright.sync_api import APIRequestContext, Page


class BasePage:
    """Base page object with UI + API capabilities."""

    def __init__(self, page: Page, api_context: APIRequestContext = None):
        self.page = page
        self.api = api_context

    def wait_for_loading(self, timeout: int = 10000) -> None:
        """Wait for spinner to disappear."""
        self.page.locator('.loading-spinner').wait_for(state='hidden', timeout=timeout)
