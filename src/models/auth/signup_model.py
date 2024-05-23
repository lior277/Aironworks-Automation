from dataclasses import dataclass


@dataclass
class EmailSignupModel:
    email: str
    password: str
    language: str
    first_name: str
    last_name: str
    company_name: str
    referral: str
