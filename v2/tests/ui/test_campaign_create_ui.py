import pytest

class TestCreateCampaign:

    @pytest.fixture(autouse=True)
    def _setup(self, api_client, auth_token):
        self.api = api_client
        self.token = auth_token

        # ---- PRECONDITION ----
        # Create customer / account
        self.account_name = random_name()
        self.account_id = self.api.create_account(self.token, self.account_name)

        yield

        # ---- CLEANUP ----
        # Delete created campaign if test created one
        if hasattr(self, "campaign_id"):
            self.api.delete_campaign(self.token, self.campaign_id)

        # Always delete account
        if hasattr(self, "account_id"):
            self.api.delete_account(self.token, self.account_id)

    def test_create_campaign_success(self):
        # ---- ACTION ----
        self.campaign_id = self.api.create_campaign(
            token=self.token,
            account_id=self.account_id,
            name="Phish | Email | Internal | EN | IT Security Notice"
        )

        # ---- ASSERT ----
        campaign = self.api.get_campaign(self.token, self.campaign_id)

        assert campaign["id"] == self.campaign_id
        assert campaign["status"] == "draft"
        assert campaign["account_id"] == self.account_id