from dataclasses import dataclass
from typing import List

from src.models.base_dataclass import BaseDataClass


@dataclass
class Assignment(BaseDataClass):
    email: str
    id: str
    portal_url: str
    status: str
    token: str


@dataclass
class EducationAssignmentsModel(BaseDataClass):
    assignments: List[Assignment]
    campaign_status: str
    limit: str
    offset: str
    total: str
