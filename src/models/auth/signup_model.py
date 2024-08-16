from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmailSignupModel(BaseDataClass):
    email: str
    password: str
    language: str
    first_name: str
    last_name: str
    company_name: str
    referral: str
