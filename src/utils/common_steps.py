import allure
from datetime import datetime, timedelta
from src.apis.education import EducationService
from src.apis.education import EducationCampaignModel
from src.utils.mailtrap import find_email
from src.configs.config_loader import AppConfigs
from playwright.sync_api import expect


@allure.step("run education campaign on employee")
def run_education_campaign_on_employee(
    api_request_context_customer_admin, mailtrap, employee
):
    result = EducationService.start_campaign(
        api_request_context_customer_admin,
        EducationCampaignModel(
            title="Automation Campaign "
            + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=[employee.employee_id],
            content_id=AppConfigs.EXAMPLE_EDUCATION_CONTENT,
        ),
    )
    expect(result).to_be_ok()

    assert "id" in result.json()
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(employee.email),
    )
    return mail
