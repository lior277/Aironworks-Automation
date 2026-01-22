"""Campaigns API client."""

from playwright.sync_api import APIResponse

from v2.src.api.routes.campaigns_routes import CampaignsRoutes
from v2.src.pages.api_pages.base_api import BaseApi


class CampaignsApi(BaseApi):
    """Campaigns API operations."""

    def get_all(self, params: dict = None) -> APIResponse:
        return self._get(CampaignsRoutes.LIST, params=params)

    def get_by_id(self, campaign_id: str) -> APIResponse:
        return self._get(CampaignsRoutes.by_id(campaign_id))

    def create(self, data: dict) -> APIResponse:
        return self._post(CampaignsRoutes.LIST, data=data)

    def update(self, campaign_id: str, data: dict) -> APIResponse:
        return self._patch(CampaignsRoutes.by_id(campaign_id), data=data)

    def delete(self, campaign_id: str) -> APIResponse:
        return self._delete(CampaignsRoutes.by_id(campaign_id))
