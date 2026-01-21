"""Campaign UI tests."""
import pytest
import allure

from v2.src.ui.pages.campaigns_page import CampaignsPage
from v2.src.api.clients.campaigns_api import CampaignsApi


@allure.feature("Campaigns")
@allure.story("UI")
class TestCampaignsUi:
    """Campaign UI tests - only deal with page objects, not auth."""

    @allure.title("Create campaign via UI")
    def test_create_campaign(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,  # For cleanup
            unique_id: str
    ):
        """Test creating a campaign via UI."""
        # Arrange
        campaign_name = f"UI_Campaign_{unique_id}"

        # Act
        create_page = campaigns_page.click_create()
        create_page.fill_name(campaign_name)
        create_page.fill_description("Created via UI test")
        create_page.click_save()

        # Assert
        campaigns_page.should_have_campaign(campaign_name)
        campaigns_page.should_have_status(campaign_name, "draft")

        # Cleanup via API (faster)
        campaigns = campaigns_api.get_all()
        campaign = next(c for c in campaigns if c.name == campaign_name)
        campaigns_api.delete(campaign.id)

    @allure.title("Search campaigns")
    def test_search_campaigns(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,
            unique_id: str
    ):
        """Test searching campaigns."""
        # Arrange - create via API (faster)
        campaign_name = f"Search_Campaign_{unique_id}"
        campaign = campaigns_api.create(name=campaign_name)
        campaigns_page.page.reload()  # Refresh to see new campaign

        # Act
        campaigns_page.search(campaign_name)

        # Assert
        campaigns_page.should_have_campaign(campaign_name)

        # Cleanup
        campaigns_api.delete(campaign.id)

    @allure.title("Delete campaign via UI")
    def test_delete_campaign(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,
            unique_id: str
    ):
        """Test deleting a campaign via UI."""
        # Arrange - create via API
        campaign_name = f"Delete_UI_Campaign_{unique_id}"
        campaigns_api.create(name=campaign_name)
        campaigns_page.page.reload()

        # Act
        campaigns_page.delete_campaign(campaign_name)

        # Assert
        campaigns_page.should_not_have_campaign(campaign_name)

    @allure.title("Filter campaigns by status")
    def test_filter_by_status(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,
            unique_id: str
    ):
        """Test filtering campaigns by status."""
        # Arrange
        campaign_name = f"Filter_UI_Campaign_{unique_id}"
        campaign = campaigns_api.create(name=campaign_name)
        campaigns_page.page.reload()

        # Act
        campaigns_page.filter_by_status("draft")

        # Assert
        campaigns_page.should_have_campaign(campaign_name)

        # Cleanup
        campaigns_api.delete(campaign.id)


@allure.feature("Campaigns")
@allure.story("E2E")
class TestCampaignsE2E:
    """End-to-end tests - UI + API verification."""

    @allure.title("Create campaign in UI, verify via API")
    def test_create_ui_verify_api(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,
            unique_id: str
    ):
        """Create in UI, verify data via API."""
        # Arrange
        campaign_name = f"E2E_Campaign_{unique_id}"

        # Act - UI
        create_page = campaigns_page.click_create()
        create_page.fill_name(campaign_name)
        create_page.fill_description("E2E test campaign")
        create_page.click_save()

        # Assert - API
        campaigns = campaigns_api.get_all()
        campaign = next((c for c in campaigns if c.name == campaign_name), None)

        assert campaign is not None, f"Campaign '{campaign_name}' not found via API"
        assert campaign.description == "E2E test campaign"

        # Cleanup
        campaigns_api.delete(campaign.id)

    @allure.title("Create campaign via API, verify in UI")
    def test_create_api_verify_ui(
            self,
            campaigns_page: CampaignsPage,
            campaigns_api: CampaignsApi,
            unique_id: str
    ):
        """Create via API, verify shows in UI."""
        # Arrange + Act - API
        campaign_name = f"API_to_UI_Campaign_{unique_id}"
        campaign = campaigns_api.create(
            name=campaign_name,
            description="Created via API"
        )

        # Assert - UI
        campaigns_page.page.reload()
        campaigns_page.search(campaign_name)
        campaigns_page.should_have_campaign(campaign_name)
        campaigns_page.should_have_status(campaign_name, "draft")

        # Cleanup
        campaigns_api.delete(campaign.id)