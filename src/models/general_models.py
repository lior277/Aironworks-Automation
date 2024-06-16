from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Data(BaseDataClass):
    success: bool


@dataclass
class BasicModel(BaseDataClass):
    data: Data


@dataclass
class LongRunningOperation(BaseDataClass):
    id: str
    status: str
    error: str = None
