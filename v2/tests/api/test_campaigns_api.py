import pytest


@pytest.mark.sanity
@pytest.mark.regression
class TestCreateCampaignApi:
    @pytest.fixture(autouse=True)
    def setup(self, campaigns_api, unique_id):
        self.campaigns_api = campaigns_api
        self.unique_id = unique_id

        self.client_id = 'client-123'

        # ---------- Precondition ----------
        self.base_campaign_id = self.campaigns_api.create_campaign(
            client_id=self.client_id, name=f'Base | {self.unique_id}'
        )

        self.campaigns_api.edit_campaign(
            campaign_id=self.base_campaign_id, name=f'Edited | {self.unique_id}'
        )

        yield

        # ---------- Teardown ----------
        if hasattr(self, 'new_campaign_id'):
            self.campaigns_api.delete_campaign(self.new_campaign_id)

        if hasattr(self, 'base_campaign_id'):
            self.campaigns_api.delete_campaign(self.base_campaign_id)

    def test_create_new_campaign(self):
        # ---------- Action ----------
        new_name = f'New | {self.unique_id}'

        self.new_campaign_id = self.campaigns_api.create_campaign(
            client_id=self.client_id, name=new_name
        )

        # ---------- Validation ----------
        campaign = self.campaigns_api.get_campaign(self.new_campaign_id)

        # ---------- Assert ----------
        assert campaign['id'] == self.new_campaign_id
        assert campaign['client_id'] == self.client_id
