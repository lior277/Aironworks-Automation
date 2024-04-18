from dataclasses import dataclass


@dataclass
class UserModel:
    email: str
    password: str
    company: str
    is_admin: str
