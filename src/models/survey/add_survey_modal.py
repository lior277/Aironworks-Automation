from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class Options(BaseDataClass):
    text: str
    has_comment: bool = None
    id: str = None
    quiz_comment: str = None


@dataclass
class Model(BaseDataClass):
    type: str
    options: list[Options]
    id: Optional[str] = None
    required: Optional[bool] = None
    title: Optional[str] = None
    correct_id: Optional[str] = None
    text: Optional[str] = None
    description: Optional[str] = None
    image_id: Optional[str] = None
    image_link: Optional[str] = None
    image_path: Optional[str] = None


@dataclass
class AddSurveyModel(BaseDataClass):
    model: list[Model]
    survey_name: str
    repeat_offence_count: Optional[int] = None
    specific_employees: Optional[list[int]] = None
