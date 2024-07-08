from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass
from src.models.education_campaign_model import EducationCampaignStatus
from src.models.survey.surveys_model import Company


@dataclass
class Item(BaseDataClass):
    id: str
    assignments_count: int
    assignments_submission_rate: int
    assignments_submitted: int
    end_date: float
    start_date: float
    execution_id: str
    status: EducationCampaignStatus
    title: str
    company: Company = None
    creator_company: Company = None


@dataclass
class EducationCampaignListModel(BaseDataClass):
    items: list[Item]
    limit: int
    offset: int
    total: int
