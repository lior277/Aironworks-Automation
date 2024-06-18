from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class LongRunningOperation(BaseDataClass):
    id: str
    status: str
    company_id: int
    error: str = None
