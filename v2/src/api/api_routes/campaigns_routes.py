"""Campaign API routes."""


class CampaignsRoutes:
    """URL routes for campaigns API."""

    LIST = "/api/campaigns"
    CREATE = "/api/campaigns"

    @staticmethod
    def detail(campaign_id: str) -> str:
        return f"/api/campaigns/{campaign_id}"

    @staticmethod
    def launch(campaign_id: str) -> str:
        return f"/api/campaigns/{campaign_id}/launch"

    @staticmethod
    def pause(campaign_id: str) -> str:
        return f"/api/campaigns/{campaign_id}/pause"