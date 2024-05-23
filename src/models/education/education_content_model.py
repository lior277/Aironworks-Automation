from dataclasses import dataclass
from typing import List

from src.models.base_dataclass import BaseDataClass


@dataclass
class Topic:
    id: int
    name: str


@dataclass
class Parts:
    kind: str
    link: str = None
    link_type: str = None
    question_type: str = None


@dataclass
class Items(BaseDataClass):
    id: str
    campaign_count: int
    date_created: float
    description: str
    industry: str
    level: str
    parts: List[Parts]
    thumbnail_path: str
    title: str
    topic: Topic


@dataclass
class EducationContentModel(BaseDataClass):
    items: List[Items]
    limit: int
    offset: int
    total: int
