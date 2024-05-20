import pytest
from playwright.sync_api import expect
from src.models.factories.user_model_factory import UserModelFactory
from src.configs.config_loader import AppConfigs
from src.utils.mailtrap import find_email


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31544"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31545"),
        ),
    ],
)
def test_create_simulation_campaign(user, employee, sign_in_page, mailtrap):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = sign_in_page.navigation_bar.navigate_scenarios()
    scenario_name = "General Scenario - English"
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.employee_table.set_filter_column("email", employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()
    execute_campaign_page.review_button.click()
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()

    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(
            employee.email,
        ),
    )

    assert mail is not None
