from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmployeeListIdsModel(BaseDataClass):
    employee_role: bool
    filters: Optional[str]
    admin_role: Optional[bool] = False
