from src.apis.admin import AdminService
from playwright.sync_api import expect
from src.configs.config_loader import AppConfigs
from src.utils.mailtrap import find_email
from src.utils.links import get_text_links

EXAMPLE_SCENARIO = "e2ced54e064a4adea24adb5a913aea83"


def test_attack_campaign(api_request_context_customer_admin, employee, mailtrap):
    result = AdminService.campaign(
        api_request_context_customer_admin,
        "Automation scenario",
        EXAMPLE_SCENARIO,
        1,
        [employee.employee_id],
    )
    expect(result).to_be_ok()
    assert "id" in result.json()
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(employee.email),
    )
    assert mail is not None

    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1
