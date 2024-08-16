from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class UserModel(BaseDataClass):
    email: str
    password: str
    is_admin: bool
    company: str = None
    is_reseller: bool = False
