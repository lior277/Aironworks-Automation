from datetime import datetime, timedelta

from src.models.education_campaign_model import EducationCampaignModel


class EducationCampaignModelFactory:
    @staticmethod
    def get_education_campaign(employee_ids: list[int],
                               content_id: str = "de69eb223d0741d49a6db2ebec93a123") -> EducationCampaignModel:
        return EducationCampaignModel(title="Automation Campaign " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                                      start_date=datetime.now().timestamp(),
                                      end_date=(datetime.now() + timedelta(days=1)).timestamp(),
                                      employee_ids=employee_ids,
                                      content_id=content_id)
