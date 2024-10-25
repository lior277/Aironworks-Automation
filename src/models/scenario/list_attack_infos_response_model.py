from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class HackerTips(BaseDataClass):
    content: str
    title: str


@dataclass
class SourceDetails(BaseDataClass):
    sender_name: str
    sender_address: Optional[str] = None
    subject: Optional[str] = None


@dataclass
class TemplateVars(BaseDataClass):
    key: str
    kind: str


@dataclass
class Infos(BaseDataClass):
    attachment_filename: str
    attachment_name: str
    attachment_path: str
    base_attack_url: str
    content: str
    date_created: float
    edit_info: str
    hacker_insight: str
    hacker_tips: list[HackerTips]
    id: str
    is_company: bool
    is_customer_generated: bool
    is_demo: bool
    is_draft: bool
    is_hidden: bool
    is_meme: bool
    kind: str
    language: str
    stats: str
    strategy_name: str
    tags: list[str]
    target_name: str
    template_vars: list[TemplateVars]
    vector: str
    version: str
    source_details: SourceDetails


@dataclass
class ListAttackInfosResponseModel(BaseDataClass):
    infos: list[Infos]
    tags: list[str]
    total: int
