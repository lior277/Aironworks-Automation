from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmployeeCountModel(BaseDataClass):
    admin_role: int
    employee_role: int
    inactive: int
