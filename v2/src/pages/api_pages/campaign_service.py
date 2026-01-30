# v2/src/api/services/campaign_service.py
from datetime import datetime, timedelta
from typing import List, Optional

from v2.src.api.api_routes.campaign_routes import CampaignRoutes
from v2.src.api.models.campaign import CampaignData, CampaignResponse
from v2.src.core.http.api_session import ApiSession


class CampaignService:
    """Service for campaign CRUD operations"""

    # Defaults as class constants
    DEFAULT_COMPANY_ID = 6332
    DEFAULT_SURVEYS = [
        'c2f6d4e5045941ad98871888ef4dae98',
        'e57108f4c5384ec7bbdf1ceafd607e1a',
    ]

    def __init__(self, session: ApiSession):
        self.session = session

    @staticmethod
    def _generate_unique_name(base_name: str) -> str:
        """Generate unique campaign name with timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        return f'{base_name}_{timestamp}'

    def create_campaign(
        self,
        scenario_id: str,
        campaign_name: str,  # REQUIRED from test
        employee_ids: List[int],  # REQUIRED from test
        company_id: Optional[int] = None,
        surveys: Optional[List[str]] = None,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        **kwargs,
    ) -> CampaignResponse:
        """
        Create campaign - campaign_name must come from test

        Args:
            scenario_id: The scenario ID
            campaign_name: Base campaign name (will be made unique)
            employee_ids: List of employee IDs
            company_id: Company ID (defaults to 6332)
            surveys: Survey IDs (defaults to predefined list)
            start_date: Unix timestamp (defaults to now)
            end_date: Unix timestamp (defaults to now + 14 days)

        Returns:
            CampaignResponse with campaign ID
        """
        # Make campaign name unique
        unique_name = self._generate_unique_name(campaign_name)

        # Apply defaults
        if company_id is None:
            company_id = self.DEFAULT_COMPANY_ID
        if surveys is None:
            surveys = self.DEFAULT_SURVEYS
        if start_date is None:
            start_date = int(datetime.now().timestamp())
        if end_date is None:
            end_date = int((datetime.now() + timedelta(days=14)).timestamp())

        # Create campaign data
        campaign_data = CampaignData(
            attack_info_id=scenario_id,
            campaign_name=unique_name,
            company_id=company_id,
            employees=employee_ids,
            surveys=surveys,
            start_date=start_date,
            end_date=end_date,
            **kwargs,
        )

        # POST to API (Pydantic auto-converts to dict with model_dump())
        response = self.session.post(
            CampaignRoutes.CREATE_CAMPAIGN,
            data=campaign_data.model_dump(),  # Pydantic method
        )

        assert response.status == 200, f'Failed to create campaign: {response.status}'

        # Parse response into typed object
        return CampaignResponse(**response.json())
