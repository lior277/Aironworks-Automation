import faker

from src.models.scenario_model import ScenarioModel

fake = faker.Faker()


class ScenarioModelFactory:
    @staticmethod
    def scenario() -> ScenarioModel:
        return ScenarioModel(
            name='QA Test Scenario ' + fake.name(),
            sender_address=fake.pystr().lower(),
            sender_name=fake.name(),
            subject=fake.sentence(),
            url_suffix=fake.pystr().lower(),
        )
