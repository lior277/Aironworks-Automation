from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


# @dataclass(unsafe_hash=True)
@dataclass()
class EmployeeModel(BaseDataClass):
    email: str
    first_name: str
    last_name: str
    employee_id: Optional[int] = None
