from datetime import datetime, timedelta

from src.models.education_campaign_model import EducationCampaignModel
from src.configs.config_loader import AppConfigs


class EducationCampaignModelFactory:
    @staticmethod
    def get_education_campaign(
        employee_ids: list[int], content_id: str = AppConfigs.EXAMPLE_EDUCATION_CONTENT
    ) -> EducationCampaignModel:
        return EducationCampaignModel(
            title="Automation Campaign "
            + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=employee_ids,
            content_id=content_id,
        )
