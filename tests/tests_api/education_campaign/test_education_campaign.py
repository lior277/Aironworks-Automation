import re
from email import message_from_bytes
from email.message import Message

import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import run_education_campaign_on_employee
from src.configs.config_loader import AppConfigs
from src.utils import markers
from src.utils.links import get_text_links


@pytest.mark.test_id("C31564")
@pytest.mark.api
@pytest.mark.smoke
def test_education_campaign(api_request_context_customer_admin, employee, mailtrap):
    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1


@pytest.mark.test_id("C31513")
@markers.common_resource(name="settings")
@pytest.mark.api
@pytest.mark.smoke
def test_education_campaign_notification_match_settings(api_request_context_customer_admin, employee, mailtrap):
    company = api.company(api_request_context_customer_admin)
    config_result = company.localized_config()
    expect(config_result).to_be_ok()
    company_config = config_result.json()
    print(company_config)

    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.raw_message(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()

    message: Message = message_from_bytes(source)
    payload = message.get_payload()

    regex_string = (
            company_config["data"][0]["education_content_publication_email"]
            .replace("{{employee.name}}", "(?P<employee_name>[a-zA-Z]+)")
            .replace(
                "{{portal_url}}",
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
            )
            + "(<img.*/>)?\n"
    )

    regex = re.compile(
        regex_string,
        re.MULTILINE,
    )

    match = regex.match(payload.replace("=\n", ""))
    assert match is not None

    assert match.group("employee_name") == employee.first_name
