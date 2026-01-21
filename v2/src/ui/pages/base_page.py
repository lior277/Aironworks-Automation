"""Base page object."""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def wait_for_loading(self) -> None:
        pass
