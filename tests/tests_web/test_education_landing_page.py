from src.utils.common_steps import run_education_campaign_on_employee
from src.utils.links import get_text_links
from src.configs.config_loader import AppConfigs
from src.page_objects.education_landing_page import EducationLandingPage
from playwright.sync_api import expect
import pytest
import json


@pytest.mark.test_id("C31535")
def test_valid_email_entry(
    api_request_context_customer_admin, employee, mailtrap, playwright_config
):
    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    new_page = playwright_config[1].new_page()
    page: EducationLandingPage = EducationLandingPage(new_page, links[0])
    page.open()

    expect(page.email_input).to_be_visible()
    page.email_input.fill(employee.email)

    expect(page.submit_button).to_be_visible()
    with page.page.expect_request_finished():
        page.submit_button.click()

    expect(page.page.get_by_text("Ongoing Content")).to_be_visible()
    expect(page.embedded_content.owner).to_be_visible()
    with pytest.raises(Exception):
        json.loads(page.iframe.content())
