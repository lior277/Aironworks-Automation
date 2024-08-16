from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Config(BaseDataClass):
    assessment_button: bool
    incident_button: bool
    assessment_button_description: str
    assessment_button_text: str
    incident_button_description: str
    incident_button_text: str
    language: str
    subtext: str


@dataclass
class AssessmentInfoModel(BaseDataClass):
    config: Config
    soc_email: str
