import faker

from src.models.scenario import CampaignType, TargetDetails
from src.models.scenario_model import ScenarioModel

fake = faker.Faker()


class ScenarioModelFactory:
    @staticmethod
    def scenario(
        campaign_type: CampaignType = CampaignType.PHISHING_LINK,
        target_details: TargetDetails = None,
    ) -> ScenarioModel:
        return ScenarioModel(
            name='QA Test Scenario ' + fake.name(),
            sender_address=fake.pystr().lower(),
            sender_name=fake.name(),
            subject=fake.sentence(),
            url_suffix=fake.pystr().lower(),
            campaign_type=campaign_type,
            target_details=target_details,
        )
