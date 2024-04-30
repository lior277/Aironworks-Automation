import pytest
from src.apis.education import EducationService
from src.apis.education import EducationCampaignModel
from datetime import datetime, timedelta
from playwright.sync_api import expect
from src.configs.config_loader import AppConfigs
from src.utils.mailtrap import find_email
from src.utils.links import get_text_links

EXAMPLE_CONTENT_ID = ""


@pytest.mark.test_id("C31564")
@pytest.mark.api
@pytest.mark.smoke
def test_education_campaign(
    api_request_context_customer_admin, api_request_context, employee, mailtrap
):
    # test /education/campaign
    result = EducationService.campaign(
        api_request_context_customer_admin,
        EducationCampaignModel(
            title="Automation Campaign "
            + datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=[employee.employee_id],
            content_id="de69eb223d0741d49a6db2ebec93a123",
        ),
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
