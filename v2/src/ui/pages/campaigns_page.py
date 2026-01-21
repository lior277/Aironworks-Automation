"""Campaigns page object."""
from playwright.sync_api import Page, expect
from v2.src.ui.pages.base_page import BasePage


class CampaignsPage(BasePage):
    """
    Campaigns list page.

    Receives Page with auth already configured.
    Test should not deal with auth - only with UI actions.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.create_button = page.locator("button:has-text('Create Campaign')")
        self.campaigns_table = page.locator("table[data-testid='campaigns-table']")
        self.search_input = page.locator("input[placeholder='Search campaigns']")
        self.status_filter = page.locator("select[data-testid='status-filter']")
        self.loading_spinner = page.locator("[data-testid='loading']")

    # =========================
    # Actions
    # =========================

    def click_create(self) -> "CreateCampaignPage":
        """Click create button, return create page."""
        self.create_button.click()
        from v2.src.ui.pages.create_campaign_page import CreateCampaignPage
        return CreateCampaignPage(self.page)

    def search(self, query: str) -> None:
        """Search campaigns by name."""
        self.search_input.clear()
        self.search_input.fill(query)
        self.search_input.press("Enter")
        self.wait_for_loading()

    def filter_by_status(self, status: str) -> None:
        """Filter campaigns by status."""
        self.status_filter.select_option(status)
        self.wait_for_loading()

    def open_campaign(self, name: str) -> "CampaignDetailsPage":
        """Click on campaign row to open details."""
        self.get_campaign_row(name).click()
        from v2.src.ui.pages.campaign_details_page import CampaignDetailsPage
        return CampaignDetailsPage(self.page)

    def delete_campaign(self, name: str) -> None:
        """Delete campaign via row action."""
        row = self.get_campaign_row(name)
        row.locator("[data-testid='delete-btn']").click()
        self.page.locator("button:has-text('Confirm')").click()
        self.wait_for_loading()

    # =========================
    # Getters
    # =========================

    def get_campaign_row(self, name: str):
        """Get campaign row by name."""
        return self.campaigns_table.locator(f"tr:has-text('{name}')")

    def get_campaign_names(self) -> list[str]:
        """Get all visible campaign names."""
        rows = self.campaigns_table.locator("tbody tr")
        return [row.locator("td:first-child").text_content() for row in rows.all()]

    def get_campaign_status(self, name: str) -> str:
        """Get status of specific campaign."""
        row = self.get_campaign_row(name)
        return row.locator("[data-testid='status']").text_content()

    # =========================
    # Assertions
    # =========================

    def should_have_campaign(self, name: str) -> None:
        """Assert campaign exists in list."""
        expect(self.get_campaign_row(name)).to_be_visible()

    def should_not_have_campaign(self, name: str) -> None:
        """Assert campaign does not exist in list."""
        expect(self.get_campaign_row(name)).not_to_be_visible()

    def should_have_status(self, name: str, status: str) -> None:
        """Assert campaign has specific status."""
        actual = self.get_campaign_status(name)
        assert actual == status, f"Expected status '{status}', got '{actual}'"

    # =========================
    # Helpers
    # =========================

    def wait_for_loading(self) -> None:
        """Wait for loading spinner to disappear."""
        expect(self.loading_spinner).not_to_be_visible(timeout=10000)