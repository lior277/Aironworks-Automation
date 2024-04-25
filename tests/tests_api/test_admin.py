import pytest
from src.apis.admin import AdminService
from src.apis.public import PublicService
from playwright.sync_api import expect
from src.configs.config_loader import AppConfigs
from src.utils.mailtrap import find_email
from src.utils.links import get_text_links, attack_url_to_api_url_input
from src.utils.waiter import wait_for
from src.models.campaign_model import CampaignModel

EXAMPLE_SCENARIO = "e2ced54e064a4adea24adb5a913aea83"


@pytest.mark.test_id("C31124")
@pytest.mark.api
@pytest.mark.smoke
def test_attack_campaign(
    api_request_context_customer_admin, api_request_context, employee, mailtrap
):
    result = AdminService.campaign(
        api_request_context_customer_admin,
        campaign=CampaignModel(
            name="Automation scenario",
            attack_info_id=EXAMPLE_SCENARIO,
            days_until_fail=1,
            employees=[employee.employee_id],
        ),
    )
    expect(result).to_be_ok()
    assert "id" in result.json()
    campaign_id = result.json()["id"]
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(employee.email),
    )
    assert mail is not None

    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    verify = PublicService.verify_url_click(
        api_request_context, url=attack_url_to_api_url_input(links[0])
    )
    expect(verify).to_be_ok()

    def validate_campaign_status():
        campaign_status = AdminService.get_attack_execution(
            api_request_context_customer_admin, campaign_id
        )
        expect(campaign_status).to_be_ok()

        return (
            campaign_status.json()["execution"]["completed"]
            and campaign_status.json()["execution"]["finished"]
        )

    assert wait_for(validate_campaign_status, 60)
