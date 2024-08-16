from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class LoginModel(BaseDataClass):
    email: str
    password: str
    remember: bool
    otp: str
    admin: bool
