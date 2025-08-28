import re
from email import message_from_bytes
from email.message import Message

import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.models.campaign_model import CampaignModel
from src.utils import markers
from src.utils.links import attack_url_to_api_url_input, get_text_links
from src.utils.log import Log
from src.utils.mailtrap import find_email
from src.utils.waiter import wait_for


@allure.step('run campaign on single employee')
def run_campaign_on_employee(
    api_request_context_customer_admin, api_request_context, mailtrap, employee
):
    admin_service = api.admin(api_request_context_customer_admin)
    public_service = api.public(api_request_context_customer_admin)
    end_date = 24  # Hours
    result = admin_service.start_campaign(
        campaign=CampaignModel(
            campaign_name='Automation scenario',
            attack_info_id=AppConfigs.EXAMPLE_SCENARIO,
            start_date=0,
            end_date=end_date * 3600,
            employees=[employee.employee_id],
        )
    )
    expect(result).to_be_ok()
    assert 'id' in result.json()
    campaign_id = result.json()['id']
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email)
    )
    assert mail is not None, (
        f'Unable to find email {employee.email} please check the mailtrap inbox {AppConfigs.EMPLOYEE_INBOX_ID}'
    )

    source = mailtrap.message_source(AppConfigs.EMPLOYEE_INBOX_ID, mail['id']).body()
    links = get_text_links(source.decode())
    assert len(links) == 1

    attack_id = attack_url_to_api_url_input(links[0])

    verify = public_service.verify_url_click(url=attack_id)
    expect(verify).to_be_ok()

    def validate_campaign_status():
        campaign_status = admin_service.get_attack_execution(campaign_id=campaign_id)
        expect(campaign_status).to_be_ok()
        print(campaign_status.json())
        return campaign_status.json()['attack_info']

    assert wait_for(validate_campaign_status, 60)


@allure.testcase('31562')
@pytest.mark.api
@pytest.mark.smoke
def test_attack_campaign(
    api_request_context_customer_admin, api_request_context, employee, mailtrap
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    run_campaign_on_employee(
        api_request_context_customer_admin, api_request_context, mailtrap, employee
    )


@allure.testcase('31511')
@markers.common_resource(name='settings')
@pytest.mark.api
@pytest.mark.smoke
def test_email_notification_match_setting(
    api_request_context_customer_admin, api_request_context, mailtrap, employee
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    company = api.company(api_request_context_customer_admin)
    config_result = company.localized_config()
    expect(config_result).to_be_ok()
    company_config = config_result.json()

    run_campaign_on_employee(
        api_request_context_customer_admin, api_request_context, mailtrap, employee
    )
    en_config = next(
        (config for config in company_config['data'] if config.get('language') == 'en'),
        None,
    )
    Log.info(
        f'waiting for email with title: {en_config["custom_attack_notification_subject"]}'
    )

    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(employee.email, en_config['custom_attack_notification_subject']),
    )
    Log.info(f'employee email: {employee.email}')

    assert mail is not None, (
        f'Unable to find email {employee.email} please check the mailtrap inbox {AppConfigs.EMPLOYEE_INBOX_ID}'
    )

    mail_id = mail['id']
    mail_raw = mailtrap.raw_message(AppConfigs.EMPLOYEE_INBOX_ID, mail_id)
    message: Message = message_from_bytes(mail_raw.body())
    payload = message.get_payload()
    Log.info('payload: \n' + payload)

    regex_string = (
        en_config['custom_attack_notification']
        .replace('="', '=3D"')
        .replace('{{employee.name}}', '(?P<employee_name>[a-zA-Z]+)')
        .replace(
            '{{portal_url}}',
            r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)',
        )
        + '(<img.*/>)?\n'
    )
    Log.info('regex_string: \n' + regex_string)

    regex = re.compile(regex_string, re.MULTILINE)

    match = regex.match(payload.replace('=\n', ''))
    assert match is not None

    assert match.group('employee_name') == employee.first_name
