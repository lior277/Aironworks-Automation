import allure

from v2.src.api.api_routes.campaigns_routes import CampaignsRoutes
from v2.src.core.http.api_session import ApiSession


class CampaignsApi:
    def __init__(self, api: ApiSession):
        self.api = api

    @allure.step('Create campaign: {name}')
    def create_campaign(self, client_id: str, name: str) -> str:
        resp = self.api.post(
            CampaignsRoutes.LIST, json={'client_id': client_id, 'name': name}
        )
        return resp.json()['id']

    @allure.step('Delete campaign: {campaign_id}')
    def delete_campaign(self, campaign_id: str) -> None:
        self.api.delete(CampaignsRoutes.by_id(campaign_id))

    @allure.step('Get campaign: {campaign_id}')
    def get_campaign(self, campaign_id: str) -> dict:
        resp = self.api.get(CampaignsRoutes.by_id(campaign_id))
        return resp.json()
