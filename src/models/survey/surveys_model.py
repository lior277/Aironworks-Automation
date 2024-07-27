from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Company(BaseDataClass):
    id: int
    name: str


@dataclass
class Survey(BaseDataClass):
    always_sent: bool
    company: Company
    date_created: float
    id: str
    name: str
    questions: str
    repeat_offence_count: int
    specific_employees: list[int]


@dataclass
class SurveysModel(BaseDataClass):
    surveys: list[Survey]

    def has_default_survey(self):
        return any(survey.always_sent for survey in self.surveys)

    def has_survey(self, survey_name: str):
        return next(
            (survey for survey in self.surveys if survey.name == survey_name), None
        )
