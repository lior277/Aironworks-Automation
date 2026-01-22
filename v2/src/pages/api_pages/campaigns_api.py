import allure


class CampaignsApi:
    def __init__(self, api_session):
        self.api = api_session

    @allure.step('Create campaign: {name}')
    def create_campaign(self, client_id: str, name: str) -> str:
        resp = self.api.post(
            '/api/campaigns', json={'client_id': client_id, 'name': name}
        )
        return resp.json()['id']

    @allure.step('Delete campaign: {campaign_id}')
    def delete_campaign(self, campaign_id: str):
        self.api.delete(f'/api/campaigns/{campaign_id}')

    @allure.step('Get campaign: {campaign_id}')
    def get_campaign(self, campaign_id: str):
        return self.api.get(f'/api/campaigns/{campaign_id}').json()
