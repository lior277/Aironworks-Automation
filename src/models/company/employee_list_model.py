from dataclasses import dataclass

from typing_extensions import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class AttackVectorModel(BaseDataClass):
    attack_vector: str
    value: str


@dataclass
class EmployeeItemModel(BaseDataClass):
    admin_role: bool
    attack_vector_addresses: list[AttackVectorModel]
    email: str
    employee_role: bool
    fields: list[str]
    first_name: str
    full_name: str
    last_name: str
    id: Optional[int]
    language: str


@dataclass
class EmployeeListModel(BaseDataClass):
    attack_vectors: list[str]
    fields: list[str]
    items: list[EmployeeItemModel]
    limit: int
    offset: int
    total: int
