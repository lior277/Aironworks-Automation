import allure
import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario import TargetDetails, TargetType
from src.models.scenario_model import ScenarioModel
from src.page_objects.scenarios_page import ScenariosPage


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id='filter scenario aw admin',
            marks=allure.testcase('31494'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='filter scenario customer admin',
            marks=allure.testcase('31496'),
        ),
    ],
)
@pytest.mark.smoke
def test_filter_scenario_by_name(user: UserModel, scenarios_page: ScenariosPage):
    filter_text = 'QA Test Scenario'
    scenarios_page.find_scenario(filter_text)
    results = scenarios_page.get_visible_results()

    for res in results:
        expect(res).to_contain_text(filter_text)


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(
                    target_type=TargetType.COMPANY,
                    target_company=AppConfigs.QA_COMPANY_NAME,
                )
            ),
            id='hide scenario',
            marks=allure.testcase('31497'),
        )
    ],
)
@pytest.mark.smoke
def test_hide_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    scenarios_page.create_scenario(scenario)
    scenario_element = scenarios_page.find_scenario(scenario.name)
    scenario_element.click()
    scenarios_page.finish_draft()
    scenarios_page.visible_tab.click()
    scenarios_page.wait_for_progress_bar_disappears()
    scenarios_page.hide_scenario.wait_for()
    scenarios_page.hide_scenario.click()
    scenarios_page.page.wait_for_load_state(timeout=5)

    expect(scenarios_page.page.get_by_text('Scenario is Hidden now')).to_be_visible()
