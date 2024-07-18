from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class Item(BaseDataClass):
    columnField: str
    operatorValue: str
    id: int
    value: str


@dataclass
class Filters(BaseDataClass):
    items: list[Item]
    linkOperator: str
    quickFilterValues: list[str]
    quickFilterLogicOperator: str


@dataclass
class EmployeeListIdsModel(BaseDataClass):
    employee_role: bool
    filters: Optional[Filters] = None
    admin_role: Optional[bool] = False
