from src.utils.common_steps import run_education_campaign_on_employee
from src.utils.links import get_text_links
from src.configs.config_loader import AppConfigs
from src.page_objects.education_landing_page import EducationLandingPage
from playwright.sync_api import expect
from src.utils.log import Log
import pytest
import json
import re
import time


@pytest.fixture(scope="function")
def new_page(playwright_config):
    new_page = playwright_config[1].new_page()
    yield new_page
    new_page.close()


@pytest.mark.test_id("C31533")
def test_valid_email_entry(
    api_request_context_customer_admin, employee, mailtrap, new_page
):
    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    page: EducationLandingPage = EducationLandingPage(new_page, links[0])
    page.open()
    page.submit_email(employee.email)

    expect(page.page.get_by_text("Ongoing Content")).to_be_visible()
    expect(page.embedded_content.owner).to_be_visible()
    with pytest.raises(Exception):
        json.loads(page.iframe.content())


@pytest.mark.test_id("C31536")
def test_submit_quiz(api_request_context_customer_admin, mailtrap, employee, new_page):
    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    Log.info("Opening page with link: " + links[0])
    Log.info("Employee email: " + employee.email)
    page: EducationLandingPage = EducationLandingPage(new_page, links[0])
    page.open()
    page.submit_email(employee.email)

    expect(page.page.get_by_text("Ongoing Content")).to_be_visible()
    expect(page.embedded_content.owner).to_be_visible()

    # Select the first question option
    page.page.locator("#field_control_0").first.click()
    page.complete_button.click()

    expect(
        page.page.get_by_role(
            "heading", name="Congratulations on completion!", exact=True
        )
    ).to_be_visible()
    expect(
        page.page.get_by_role("heading", name="100 /100", exact=True)
    ).to_be_visible()
    new_page.close()


@pytest.mark.test_id("C31535")
def test_iframe_is_correct(
    api_request_context_customer_admin, mailtrap, employee, new_page
):
    mail = run_education_campaign_on_employee(
        api_request_context_customer_admin, mailtrap, employee
    )
    assert mail is not None
    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail["id"]).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    Log.info("Opening page with link: " + links[0])
    Log.info("Employee email: " + employee.email)
    page: EducationLandingPage = EducationLandingPage(new_page, links[0])
    page.open()
    page.submit_email(employee.email)

    expect(page.page.get_by_text("Ongoing Content")).to_be_visible()

    assert re.compile("https://www.youtube.com/embed/.*").match(page.iframe.url)
