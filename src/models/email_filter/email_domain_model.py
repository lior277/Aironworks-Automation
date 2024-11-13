from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class EmailDomainModel(BaseDataClass):
    email_address: str
    domain: str
