from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Filters(BaseDataClass):
    key: str
    value: str


@dataclass
class ListAttackInfosModel(BaseDataClass):
    end_index: int
    filters: list[Filters]
    start_index: int = 0
