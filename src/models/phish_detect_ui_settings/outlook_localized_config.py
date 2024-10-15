from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class OutlookConfigData(BaseDataClass):
    assessment_button: Optional[bool] = None
    assessment_button_description: Optional[str] = None
    assessment_button_text: Optional[str] = None
    incident_button: Optional[bool] = None
    incident_button_description: Optional[str] = None
    incident_button_text: Optional[str] = None
    language: Optional[str] = None
    subtext: Optional[str] = None


@dataclass
class OutlookLocalizedConfig(BaseDataClass):
    data: list[OutlookConfigData]
