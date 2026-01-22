"""Campaigns API routes."""


class CampaignsRoutes:
    LIST = '/api/campaigns'

    @staticmethod
    def by_id(campaign_id: str) -> str:
        return f'/api/campaigns/{campaign_id}'
