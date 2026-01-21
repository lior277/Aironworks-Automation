import pytest


@pytest.mark.sanity
@pytest.mark.regression
class TestEditCreateDeleteCampaignApi:
    @pytest.fixture(autouse=True)
    def setup(self, api_factory, crm_url, campaign_api):
        """
        This is:
        - [SetUp]
        - DI (dependency injection)
        - [TearDown]
        in one place
        """
        self.api_factory = api_factory
        self.crm_url = crm_url
        self.campaign_api = campaign_api

        self.client_id = 'client-123'  # normally created via ClientsApi

        # =========================
        # PreCondition
        # =========================

        # create base campaign
        self.base_campaign_id = self.campaign_api.create_campaign(
            self.crm_url, self.client_id, f'Base | {random_string()}'
        )

        # edit existing campaign (as you asked)
        self.campaign_api.edit_campaign(
            self.crm_url, self.base_campaign_id, f'Edited | {random_string()}'
        )

        yield

        # =========================
        # TearDown
        # =========================

        if hasattr(self, 'new_campaign_id'):
            self.campaign_api.delete_campaign(self.crm_url, self.new_campaign_id)

        if hasattr(self, 'base_campaign_id'):
            self.campaign_api.delete_campaign(self.crm_url, self.base_campaign_id)

    # =========================
    # Test (STORY)
    # =========================
    def test_create_new_campaign(self):
        # ---- Action ----
        new_name = f'New | {random_string()}'

        self.new_campaign_id = self.campaign_api.create_campaign(
            self.crm_url, self.client_id, new_name
        )

        # ---- Validation ----
        campaign = self.campaign_api.get_campaign(self.crm_url, self.new_campaign_id)

        # ---- Assert ----
        assert campaign['id'] == self.new_campaign_id
        assert campaign['client_id'] == self.client_id
