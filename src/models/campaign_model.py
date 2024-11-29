from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CampaignModel:
    campaign_name: str
    attack_info_id: str
    employees: List[int]
    attack_url: str = None
    start_date: str = None
    custom_reminder: int = None
    content_id: str = None
    special: List[str] = field(default_factory=list)
    company_id: Optional[int] = None
    send_attacks: Optional[bool] = True
    end_date: str = None
