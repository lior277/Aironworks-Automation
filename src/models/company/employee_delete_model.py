from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmployeeDeleteModel(BaseDataClass):
    ids: list[int]
