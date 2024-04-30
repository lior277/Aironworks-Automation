from dataclasses import dataclass
from typing import List
from enum import Enum


class EducationCampaignStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"


@dataclass
class EducationCampaignModel:
    title: str
    start_date: int  # timestamp
    end_date: int
    content_id: str
    score_required: int = 0
    company_id: int = None
    all_employees: bool = False
    employee_ids: List[int] = None
    phishing_campaign_ids: List[str] = None
    reminder_dates: List[int] = None
