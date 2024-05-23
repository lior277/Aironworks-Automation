import faker
import pytest
from playwright.sync_api import expect

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario_model import ScenarioModel
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage

fake = faker.Faker()


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
@pytest.mark.smoke
def test_create_scenario(user: UserModel, scenario, sign_in_page: SignInPage, dashboard_page: DashboardPage):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigation_bar.navigate_scenarios()

    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="filter scenario aw admin",
            marks=pytest.mark.test_id("C31494"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="filter scenario customer admin",
            marks=pytest.mark.test_id("C31496"),
        ),
    ],
)
@pytest.mark.smoke
def test_filter_scenario_by_name(user: UserModel, sign_in_page, dashboard_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigation_bar.navigate_scenarios()

    filter_text = "QA Test Scenario"

    scenarios_page.find_scenario(filter_text)

    results = scenarios_page.get_visible_results()

    for res in results:
        expect(res).to_contain_text(filter_text)


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
@pytest.mark.smoke
def test_hide_scenario(user: UserModel, scenario: ScenarioModel, sign_in_page: SignInPage,
                       dashboard_page: DashboardPage):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigation_bar.navigate_scenarios()
    scenarios_page.create_scenario(scenario)

    scenario_element = scenarios_page.find_scenario(scenario.name)

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
@pytest.mark.smoke
def test_clone_scenario(user: UserModel, scenario, sign_in_page, dashboard_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigation_bar.navigate_scenarios()
    scenarios_page.create_scenario(scenario)

    scenario_element = scenarios_page.find_scenario(scenario.name)
    scenario_element.click()
    scenario_element.page.wait_for_load_state(timeout=5)

    scenarios_page.page.get_by_role("button", name="Clone").click()
    scenario_element.page.wait_for_load_state(timeout=5)

    scenario.name = fake.sentence()
    scenario.html_content = "{{attack_url}} " + fake.sentence()

    scenarios_page.submit_create_scenario_form(scenario, clone_mode=True)
