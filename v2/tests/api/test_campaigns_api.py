"""Campaign API tests."""
import pytest
import allure

from v2.src.api.clients.campaigns_api import CampaignsApi


@allure.feature("Campaigns")
@allure.story("API")
class TestCampaignsApi:
    """Campaign API tests - only deal with API client, not auth."""

    @allure.title("Create campaign via API")
    def test_create_campaign(self, campaigns_api: CampaignsApi, unique_id: str):
        """Test creating a campaign via API."""
        # Arrange
        campaign_name = f"API_Campaign_{unique_id}"

        # Act
        campaign = campaigns_api.create(
            name=campaign_name,
            description="Created via API test"
        )

        # Assert
        assert campaign.id is not None
        assert campaign.name == campaign_name
        assert campaign.status == "draft"

        # Cleanup
        campaigns_api.delete(campaign.id)

    @allure.title("Get campaign by ID")
    def test_get_campaign_by_id(self, campaigns_api: CampaignsApi, unique_id: str):
        """Test getting campaign by ID."""
        # Arrange - create campaign first
        campaign_name = f"Get_Campaign_{unique_id}"
        created = campaigns_api.create(name=campaign_name)

        # Act
        fetched = campaigns_api.get_by_id(created.id)

        # Assert
        assert fetched.id == created.id
        assert fetched.name == campaign_name

        # Cleanup
        campaigns_api.delete(created.id)

    @allure.title("Update campaign")
    def test_update_campaign(self, campaigns_api: CampaignsApi, unique_id: str):
        """Test updating a campaign."""
        # Arrange
        campaign = campaigns_api.create(name=f"Update_Campaign_{unique_id}")
        new_name = f"Updated_Campaign_{unique_id}"

        # Act
        updated = campaigns_api.update(campaign.id, name=new_name)

        # Assert
        assert updated.name == new_name

        # Cleanup
        campaigns_api.delete(campaign.id)

    @allure.title("Delete campaign")
    def test_delete_campaign(self, campaigns_api: CampaignsApi, unique_id: str):
        """Test deleting a campaign."""
        # Arrange
        campaign = campaigns_api.create(name=f"Delete_Campaign_{unique_id}")

        # Act
        campaigns_api.delete(campaign.id)

        # Assert - should not find deleted campaign
        all_campaigns = campaigns_api.get_all()
        assert not any(c.id == campaign.id for c in all_campaigns)

    @allure.title("List campaigns with filter")
    def test_list_campaigns_with_filter(self, campaigns_api: CampaignsApi, unique_id: str):
        """Test listing campaigns with status filter."""
        # Arrange
        campaign = campaigns_api.create(name=f"Filter_Campaign_{unique_id}")

        # Act
        draft_campaigns = campaigns_api.get_all(status="draft")

        # Assert
        assert any(c.id == campaign.id for c in draft_campaigns)

        # Cleanup
        campaigns_api.delete(campaign.id)