# v2/src/api/models/campaign.py
from typing import List, Optional

from pydantic import BaseModel


class CampaignData(BaseModel):
    """Data model for creating campaigns"""

    attack_info_id: str
    campaign_name: str
    company_id: int
    employees: List[int]
    start_date: int
    end_date: int
    surveys: List[str]
    special: List[str] = []
    attack_url: Optional[str] = None
    content_id: Optional[str] = None


class CampaignResponse(BaseModel):
    """Response model from POST campaign API"""

    id: str  # or int, depending on actual response
    campaign_name: str
    # Add other fields from actual response
