from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Group(BaseDataClass):
    date_created: float
    employee_ids: list[int]
    manager_ids: list[int]
    id: str
    name: str
    num_employees: int
    num_managers: int
    some_employee_names: list[str]
    some_manager_names: list[str]


@dataclass
class GroupListModel(BaseDataClass):
    groups: list[Group]


@dataclass
class GroupDetailsModel(BaseDataClass):
    group: Group
