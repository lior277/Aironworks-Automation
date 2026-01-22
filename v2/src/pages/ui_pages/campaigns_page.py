"""Campaigns page object."""

from playwright.sync_api import APIRequestContext, Locator, Page

from v2.src.api.routes.campaigns_routes import CampaignsRoutes
from v2.src.pages.ui_pages.base_page import BasePage


class CampaignsPage(BasePage):
    """Campaigns list page."""

    def __init__(self, page: Page, api_context: APIRequestContext = None):
        super().__init__(page, api_context)

        # Locators
        self.create_button = page.get_by_role('button', name='Create')
        self.search_input = page.get_by_placeholder('Search')
        self.table = page.locator('table')

    # ─────────────────────────────────────────────
    # UI Actions
    # ─────────────────────────────────────────────

    def click_create(self) -> 'CreateCampaignPage':
        self.create_button.click()
        from v2.src.pages import CreateCampaignPage

        return CreateCampaignPage(self.page, self.api)

    def search(self, text: str) -> None:
        self.search_input.fill(text)
        self.search_input.press('Enter')
        self.wait_for_loading()

    def get_row(self, name: str) -> Locator:
        return self.table.locator('tr', has_text=name)

    # ─────────────────────────────────────────────
    # API Actions (hybrid)
    # ─────────────────────────────────────────────

    def get_campaigns_via_api(self) -> list:
        """Get campaigns list via API."""
        if not self.api:
            raise RuntimeError('API context not provided')
        response = self.api.get(CampaignsRoutes.LIST)
        return response.json().get('items', [])

    def delete_campaign_via_api(self, campaign_id: str) -> None:
        """Delete campaign via API."""
        if not self.api:
            raise RuntimeError('API context not provided')
        self.api.delete(CampaignsRoutes.by_id(campaign_id))
