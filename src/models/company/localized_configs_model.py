from dataclasses import dataclass

from src.models.base_dataclass import BaseDataClass


@dataclass
class Data(BaseDataClass):
    custom_attack_notification: str
    custom_attack_notification_sender: str
    custom_attack_notification_subject: str
    custom_failed_attack_notification: str
    custom_failed_attack_notification_sender: str
    custom_failed_attack_notification_subject: str
    custom_survey_review_email: str
    custom_survey_review_sender: str
    custom_survey_review_subject: str
    education_content_publication_email: str
    education_content_publication_sender: str
    education_content_publication_subject: str
    education_content_reminder_email: str
    education_content_reminder_sender: str
    education_content_reminder_subject: str
    language: str
    light_mode: bool
    show_survey_button: bool
    survey_reminder_email: str
    survey_reminder_interval: int
    survey_reminder_sender: str
    survey_reminder_subject: str
    custom_sd_body: str
    custom_sd_logo_name: str
    custom_sd_logo_url: str
    custom_sd_warning: str


@dataclass
class LocalizedConfigsModel(BaseDataClass):
    data: list[Data]
