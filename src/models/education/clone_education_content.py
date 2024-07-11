from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass
from src.models.education.education_content_model import Part


@dataclass
class CloneEducationContentModel(BaseDataClass):
    any_company: bool
    description: str
    level: str
    parts: list[Part]
    title: str
    topic_name: str
    thumbnail_path: str = None
    company_ids: list[int] = None
