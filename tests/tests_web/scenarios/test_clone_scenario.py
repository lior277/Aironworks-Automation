import faker
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario import ScenarioCloneMode
from src.models.scenario_model import ScenarioModel
from src.page_objects.scenarios_page import ScenariosPage

fake = faker.Faker()


@pytest.mark.parametrize(
    'user,scenario,clone_mode',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(),
            ScenarioCloneMode.NEW_BODY,
            id='test clone scenario with editing customer admin',
            marks=pytest.mark.test_id('C31492'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(),
            ScenarioCloneMode.NEW_BODY,
            id='test clone scenario with editing aw admin',
            marks=pytest.mark.test_id('C31491'),
        ),
    ],
)
@pytest.mark.smoke
def test_clone_scenario(
    user: UserModel,
    scenario: ScenarioModel,
    scenarios_page: ScenariosPage,
    clone_mode: ScenarioCloneMode,
):
    scenarios_page.create_scenario(scenario)

    scenario_element = scenarios_page.find_scenario(scenario.name)
    scenario_element.click()

    scenarios_page.page.get_by_role('button', name='Clone').click()

    scenario.name = fake.sentence()
    scenario.html_content = '{{attack_url}} ' + fake.sentence()

    scenarios_page.submit_create_scenario_form(scenario, clone_mode=clone_mode)
