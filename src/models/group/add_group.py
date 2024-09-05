from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class AddGroupModel(BaseDataClass):
    name: str
    employee_ids: list[int]
    manager_ids: list[int]
    edit_id: Optional[int] = None
