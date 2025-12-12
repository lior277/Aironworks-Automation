import os

import allure
import faker
import pytest

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario import ScenarioCloneMode, TargetDetails, TargetType
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
            marks=allure.testcase('31492'),
        ),
        pytest.param(
            UserModelFactory.encrypted_customer_admin(),
            ScenarioModelFactory.scenario(),
            ScenarioCloneMode.NEW_BODY,
            id='test clone scenario with editing encrypted customer admin',
            marks=[
                allure.testcase('31492'),
                pytest.mark.skipif(
                    os.getenv('ENV') != 'staging', reason='Staging only'
                ),
            ],
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(
                    target_type=TargetType.EMPLOYEE,
                    target_company=AppConfigs.QA_COMPANY_NAME,
                )
            ),
            ScenarioCloneMode.NEW_BODY,
            id='test clone scenario with editing aw admin',
            marks=allure.testcase('31491'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(),
            ScenarioCloneMode.COPY_CONTENT,
            id='test clone scenario via copy content customer admin',
            marks=allure.testcase('31777'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(
                    target_type=TargetType.EMPLOYEE,
                    target_company=AppConfigs.QA_COMPANY_NAME,
                )
            ),
            ScenarioCloneMode.COPY_CONTENT,
            id='test clone scenario via copy content aw admin',
            marks=allure.testcase('31778'),
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
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    scenarios_page.create_scenario(scenario)

    scenario_element = scenarios_page.find_scenario(scenario.name)
    scenario_element.click()

    scenarios_page.page.get_by_role('button', name='Clone').click()
    scenarios_page.verify_cloned_scenario_form(scenario)
    scenario.name = fake.sentence()
    if clone_mode == ScenarioCloneMode.NEW_BODY:
        scenario.html_content = '{{attack_url}} ' + fake.sentence()

    scenarios_page.submit_create_scenario_form(scenario, clone_mode=clone_mode)
