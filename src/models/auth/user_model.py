from dataclasses import dataclass


@dataclass
class UserModel:
    email: str
    password: str
    is_admin: bool
    company: str = None
    is_reseller: bool = False
