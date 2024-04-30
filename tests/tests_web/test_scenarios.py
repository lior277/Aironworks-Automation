import pytest
from playwright.sync_api import expect
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.login_page import SignInPage
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.factories.user_model_factory import UserModelFactory


@pytest.mark.parametrize(
    "user,scenario",
    [
        pytest.param(
            UserModelFactory.my_user(),
            ScenarioModelFactory.scenario(),
            id="test create scenario customer admin",
            marks=pytest.mark.test_id("C31490"),
        )
    ],
)
def test_create_scenario(
    user, scenario, sign_in_page: SignInPage, dashboard_page: DashboardPage
):
    sign_in_page.navigate()
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = dashboard_page.navigate_scenarios()

    scenarios_page.navigate_create_scenario()

    scenarios_page.submit_create_scenario_form(scenario)

    expect(scenarios_page.page.get_by_text("Created new scenario")).to_be_visible()
