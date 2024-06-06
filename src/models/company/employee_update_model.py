from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmployeeUpdateModel(BaseDataClass):
    employee_role: bool
    ids: list[int]
