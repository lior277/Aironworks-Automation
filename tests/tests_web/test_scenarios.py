import pytest
from playwright.sync_api import expect
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage
from src.page_objects.scenarios_page import ScenariosPage
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario_model import ScenarioModel
from src.models.factories.user_model_factory import UserModelFactory
import re
import allure
import faker

fake = faker.Faker()


@allure.step("Create scenario")
def step_create_scenario(scenarios_page, scenario: ScenarioModel):
    scenarios_page.navigate_create_scenario()

    scenarios_page.submit_create_scenario_form(scenario)

    expect(scenarios_page.page.get_by_text("Created new scenario")).to_be_visible()


@allure.step("Find scenario")
def step_find_scenario(scenarios_page, scenario: ScenarioModel):
    scenarios_page.filter_by_name(scenario.name)
    scenarios_page.filter_by_language("All")
    scenarios_page.wait_sync_filters()
    scenario = (
        scenarios_page.page.get_by_role("button")
        .filter(has_text=re.compile(scenario.name))
        .first
    )
    expect(scenario).to_be_visible()
    return scenario


@pytest.mark.parametrize(
    "user,scenario",
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(),
            id="test create scenario customer admin",
            marks=pytest.mark.test_id("C31490"),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(),
            id="test create scenario aw admin",
            marks=pytest.mark.test_id("C31489"),
        ),
    ],
)
def test_create_scenario(
    user, scenario, sign_in_page: SignInPage, dashboard_page: DashboardPage
):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigate_scenarios()

    step_create_scenario(scenarios_page, scenario)


@pytest.mark.parametrize(
    "user,scenario",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(),
            id="hide scenario",
            marks=pytest.mark.test_id("C31497"),
        )
    ],
)
def test_hide_scenario(
    user, scenario, sign_in_page: SignInPage, dashboard_page: DashboardPage
):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigate_scenarios()
    step_create_scenario(scenarios_page, scenario)

    scenario_element = step_find_scenario(scenarios_page, scenario)

    scenario_element.click()
    scenarios_page.finish_draft()

    scenarios_page.visible_tab.click()
    scenarios_page.wait_sync_filters()

    scenarios_page.hide_scenario.click()
    scenarios_page.page.wait_for_load_state(timeout=5)

    expect(scenarios_page.page.get_by_text("Scenario is Hidden now")).to_be_visible()


@pytest.mark.parametrize(
    "user,scenario",
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(),
            id="test create scenario customer admin",
            marks=pytest.mark.test_id("C31492"),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(),
            id="test create scenario aw admin",
            marks=pytest.mark.test_id("C31491"),
        ),
    ],
)
def test_clone_scenario(user, scenario, sign_in_page, dashboard_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigate_scenarios()
    step_create_scenario(scenarios_page, scenario)

    scenario_element = step_find_scenario(scenarios_page, scenario)
    scenario_element.click()
    scenario_element.page.wait_for_load_state(timeout=5)

    scenarios_page.page.get_by_role("button", name="Clone").click()
    scenario_element.page.wait_for_load_state(timeout=5)

    scenario.name = fake.sentence()
    scenario.html_content = "{{attack_url}} " + fake.sentence()

    scenarios_page.submit_create_scenario_form(scenario, clone_mode=True)
