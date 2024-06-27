from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CampaignModel:
    campaign_name: str
    attack_info_id: str
    days_until_fail: int
    employees: List[int]
    attack_url: str = None
    attack_date: str = None
    custom_reminder: int = None
    content_id: str = None
    special: List[str] = field(default_factory=list)
    company_id: Optional[int] = None
