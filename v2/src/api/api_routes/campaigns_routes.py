"""Campaigns API routes."""


class CampaignsRoutes:
    BASE = '/api/campaigns'

    @classmethod
    def list(cls) -> str:
        return cls.BASE

    @classmethod
    def by_id(cls, campaign_id: str) -> str:
        return f'{cls.BASE}/{campaign_id}'
