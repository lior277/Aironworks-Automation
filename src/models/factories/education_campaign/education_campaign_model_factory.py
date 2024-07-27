import random
from datetime import datetime, timedelta

from src.configs.config_loader import AppConfigs
from src.models.education_campaign_model import EducationCampaignModel


class EducationCampaignModelFactory:
    @staticmethod
    def get_education_campaign(
        employee_ids: list[int], content_id: str = AppConfigs.EXAMPLE_EDUCATION_CONTENT
    ) -> EducationCampaignModel:
        return EducationCampaignModel(
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=employee_ids,
            content_id=content_id,
        )

    @staticmethod
    def get_education_campaign_from_education_content(
        education_content_id: str, employee_ids: list[int]
    ) -> EducationCampaignModel:
        return EducationCampaignModel(
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            + ''.join(
                random.choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k=5)
            ),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=employee_ids,
            content_id=education_content_id,
        )
