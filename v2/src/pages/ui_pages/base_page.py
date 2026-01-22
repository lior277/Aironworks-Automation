"""Base page with optional API context."""

from playwright.sync_api import APIRequestContext, Page


class BasePage:
    """Base page object with UI + optional API capabilities."""

    def __init__(self, page: Page, api_context: APIRequestContext | None = None):
        self.page = page
        self.api = api_context

    def wait_for_loading(self, timeout: int = 10_000) -> None:
        """Wait for spinner/overlay to disappear (best-effort).

        Adjust the selector to your app once you confirm it in DevTools.
        """
        selectors = [
            '.loading-spinner',
            "[data-testid='loading']",
            '.MuiCircularProgress-root',
            '.MuiBackdrop-root',
        ]
        for sel in selectors:
            try:
                self.page.locator(sel).first.wait_for(state='hidden', timeout=timeout)
                return
            except Exception:
                continue
        # If no known spinner found, do nothing (do not fail tests)
