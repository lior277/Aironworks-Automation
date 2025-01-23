import allure
import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, header_key, header_value',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'X-AIRONWORKS-SECRET-HEADER',
            'This is test header for Aironworks',
            marks=allure.testcase('C31866'),
        )
    ],
)
def test_email_sending(
    training_settings_email_sending_page,
    user: UserModel,
    header_key,
    header_value,
    request,
    mailtrap,
    employee,
):
    training_settings_email_sending_page.enable_email_header_settings(
        header_key, header_value
    )
    scenarios_page = (
        training_settings_email_sending_page.navigation_bar.navigate_scenarios()
    )
    scenario_name = AppConfigs.EXAMPLE_SCENARIO_NAME
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.employee_table.set_filter_column('email', employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()
    execute_campaign_page.review_button.click()
    assert execute_campaign_page.number_of_employees.text_content() == '1'
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()
    mailtrap.check_custom_header(
        AppConfigs.EMPLOYEE_INBOX_ID, employee.email, header_key, header_value
    )
    execute_campaign_page.navigation_bar.navigate_training_settings_email_sending_page()
    training_settings_email_sending_page.disable_email_header_settings()
