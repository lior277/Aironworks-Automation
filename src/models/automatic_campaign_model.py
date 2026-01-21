from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AutomaticCampaignModel:
    operation_name: str
    vector_type: str
    scenarios: List[str]
    employees: List[str]
    execution_date: str
    completion_date: str
    frequency: str
    scenarios_employee: str
    interval: str
    content: List[str]
    survey: List[str]
    campaign_duration: Optional[str] = None
    range_start_time: Optional[str] = None
    range_end_time: Optional[str] = None
