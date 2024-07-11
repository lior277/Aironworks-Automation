from dataclasses import dataclass
from typing import List

from src.models.base_dataclass import BaseDataClass


@dataclass
class RecentCampaigns(BaseDataClass):
    id: str
    title: str


@dataclass
class Industry(BaseDataClass):
    id: int
    name: str


@dataclass
class Topic(BaseDataClass):
    id: int
    name: str


@dataclass
class Part(BaseDataClass):
    kind: str
    link: str = None
    link_type: str = None
    question_type: str = None
    correct: list[int] = None
    description: str = None
    options: list[str] = None
    question: str = None
    required: bool = None
    score: int = None
    title: str = None


@dataclass
class Item(BaseDataClass):
    id: str
    campaign_count: int
    date_created: float
    description: str
    level: str
    parts: list[Part]
    title: str
    topic: Topic
    thumbnail_path: str = None
    any_company: bool = None
    companies: list[int] = None
    industry: Industry = None
    sensitive: bool = None
    recent_campaigns: list[RecentCampaigns] = None
    editable: bool = None


@dataclass
class EducationContentModel(BaseDataClass):
    items: List[Item]
    limit: int
    offset: int
    total: int
