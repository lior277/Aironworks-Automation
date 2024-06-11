from src.models.campaign_model import CampaignModel


class CampaignModelFactory:

    @staticmethod
    def get_campaign(name: str, company_id: int, employees: list[int], attack_info_id: str) -> CampaignModel:
        return CampaignModel(name=name, company_id=company_id, days_until_fail=1, employees=employees,
                             attack_info_id=attack_info_id)
