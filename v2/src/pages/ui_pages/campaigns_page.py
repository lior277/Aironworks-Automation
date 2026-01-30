"""Campaigns page object."""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class CampaignsPage:
    def __init__(self, page: Page):
        self.page = page  # FIXED: Store the page directly, no super().__init__

        # TODO: update selectors to match your app
        self.search_input: Locator = page.get_by_role('textbox').first
        self.create_button: Locator = page.get_by_role('button', name='Create')
        self.save_button: Locator = page.get_by_role('button', name='Save')
        self.name_input: Locator = page.locator("input[name='name']")
        self.description_input: Locator = page.locator("textarea[name='description']")

    def open(self) -> 'CampaignsPage':
        # FIXED: Implement goto directly
        from v2.src.core.config import Config

        self.page.goto(
            f'{Config.APP_BASE_URL}/campaigns', wait_until='domcontentloaded'
        )
        self.page.wait_for_load_state('domcontentloaded')
        return self

    def create(self, *, name: str, description: str) -> None:
        self.create_button.click()
        self.name_input.fill(name)
        self.description_input.fill(description)
        self.save_button.click()

    def search(self, text: str) -> None:
        self.search_input.fill(text)
        self.search_input.press('Enter')

    def assert_visible(self, name: str) -> None:
        expect(self.page.get_by_text(name)).to_be_visible()

    def assert_not_visible(self, name: str) -> None:
        expect(self.page.get_by_text(name)).not_to_be_visible()
