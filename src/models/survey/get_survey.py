from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass
from src.models.survey.surveys_model import Company


@dataclass
class Option(BaseDataClass):
    has_comment: bool
    hide_time: bool
    id: str
    quiz_comment: str
    text: str


@dataclass
class Question(BaseDataClass):
    correct_id: str
    description: str
    hide_time: bool
    id: str
    image_id: str
    image_link: str
    image_path: str
    options: list[Option]
    required: bool
    text: str
    title: str
    type: str


@dataclass
class Model(BaseDataClass):
    always_sent: bool
    company: Company
    date_created: float
    id: str
    name: str
    questions: list[Question]
    repeat_offence_count: int
    specific_employees: list[int]


@dataclass
class GetSurveyModel(BaseDataClass):
    model: Model
    timestamp: float
