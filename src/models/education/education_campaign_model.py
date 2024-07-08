from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass
from src.models.education.education_content_model import Part
from src.models.survey.surveys_model import Company


@dataclass
class Content(BaseDataClass):
    id: str
    title: str
    parts: list[Part]


@dataclass
class EducationCampaignDetailsModel(BaseDataClass):
    assignments_count: int
    assignments_submission_rate: float
    assignments_submitted: int
    average_score: str
    average_total: float
    content: Content
    end_date: float
    execution_id: str
    id: str
    reminders: list[str]
    score_required: float
    start_date: float
    status: str
    title: str
    company: Company = None
