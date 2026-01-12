from datetime import datetime, timedelta

import faker

from src.models.automatic_campaign_model import AutomaticCampaignModel

fake = faker.Faker()


class AutomaticCampaignModelFactory:
    @staticmethod
    def get_automatic_campaign() -> AutomaticCampaignModel:
        return AutomaticCampaignModel(
            operation_name='Test Automatic Campaign 123#@!',
            vector_type='Email',
            scenarios=['Duc Color Scenario', 'Test Scenario 2'],
            employees=['pham.duc@aironworks.com', 'Test Employee 2'],
            execution_date=(datetime.now() + timedelta(days=1)).strftime(
                '%m/%d/%Y %H:%M'
            ),
            completion_date=(datetime.now() + timedelta(days=8)).strftime(
                '%m/%d/%Y %H:%M'
            ),
            frequency='Daily',
            scenarios_employee='2',
            interval='1',
            content='Multiple Quiz',
            survey='Default Survey',
            campaign_duration='3',
            range_start_time='00:00',
            range_end_time='23:59',
        )
