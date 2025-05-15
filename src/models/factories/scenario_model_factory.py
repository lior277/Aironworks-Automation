import faker

from src.models.scenario import CampaignType, TargetDetails
from src.models.scenario_model import ScenarioModel
from src.utils.text_gen import generate_faker_multiline_text

fake = faker.Faker()


class ScenarioModelFactory:
    @staticmethod
    def scenario(
        vector: str = 'Email',
        campaign_type: CampaignType = CampaignType.PHISHING_LINK,
        target_details: TargetDetails = None,
        file_path: str = None,
        html_content="""{{attack_url}}  """,
        custom_text=generate_faker_multiline_text(lines=5),
    ) -> ScenarioModel:
        return ScenarioModel(
            name='QA Test Scenario ' + fake.name(),
            vector=vector,
            sender_address=fake.pystr().lower(),
            sender_name=fake.name(),
            subject=fake.sentence(),
            url_suffix=fake.pystr().lower(),
            campaign_type=campaign_type,
            target_details=target_details,
            file_path=file_path,
            html_content=html_content,
            custom_text=custom_text,
        )
