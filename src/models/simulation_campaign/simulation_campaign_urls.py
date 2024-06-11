from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Attack(BaseDataClass):
    attack_url: str
    email: str
    id: str
    status: str


@dataclass
class CampaignUrls(BaseDataClass):
    attacks: list[Attack]
    completed: bool
    finished: bool
    limit: int
    offset: str
    pending: bool
    started: bool
    total: int
