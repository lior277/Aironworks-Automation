from dataclasses import dataclass


@dataclass
class UserModel:
    email: str
    password: str
    is_admin: str
    company: str = None
