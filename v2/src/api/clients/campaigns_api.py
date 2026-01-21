"""Campaigns API client."""

from typing import Optional

from v2.src.api.api_routes.campaigns_routes import CampaignsRoutes
from v2.src.core.http.api_session import ApiSession


class CampaignsApi:
    """
    Campaigns API client.

    Receives ApiSession with auth already configured.
    Test should not deal with auth - only with business logic.
    """

    def __init__(self, session: ApiSession):
        self.session = session
        self.routes = CampaignsRoutes()

    def get_all(self, status: Optional[str] = None) -> list[Campaign]:
        """Get all campaigns, optionally filtered by status."""
        params = {'status': status} if status else {}
        response = self.session.get(self.routes.LIST, params=params)
        response.raise_for_status()
        return [Campaign(**c) for c in response.json()['items']]

    def get_by_id(self, campaign_id: str) -> Campaign:
        """Get campaign by ID."""
        response = self.session.get(self.routes.detail(campaign_id))
        response.raise_for_status()
        return Campaign(**response.json())

    def create(self, name: str, description: str = '', **kwargs) -> Campaign:
        """Create new campaign."""
        data = CreateCampaignRequest(name=name, description=description, **kwargs)
        response = self.session.post(self.routes.CREATE, json=data.to_dict())
        response.raise_for_status()
        return Campaign(**response.json())

    def update(self, campaign_id: str, **kwargs) -> Campaign:
        """Update existing campaign."""
        data = UpdateCampaignRequest(**kwargs)
        response = self.session.put(
            self.routes.detail(campaign_id), json=data.to_dict()
        )
        response.raise_for_status()
        return Campaign(**response.json())

    def delete(self, campaign_id: str) -> None:
        """Delete campaign."""
        response = self.session.delete(self.routes.detail(campaign_id))
        response.raise_for_status()

    def launch(self, campaign_id: str) -> Campaign:
        """Launch campaign."""
        response = self.session.post(self.routes.launch(campaign_id))
        response.raise_for_status()
        return Campaign(**response.json())

    def pause(self, campaign_id: str) -> Campaign:
        """Pause campaign."""
        response = self.session.post(self.routes.pause(campaign_id))
        response.raise_for_status()
        return Campaign(**response.json())
