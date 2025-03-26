import random
import re
from base64 import b64encode

import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.utils.log import Log
from src.utils.mailtrap import find_email
from src.utils.waiter import wait_for_lro


@pytest.mark.parametrize(
    'user', [UserModelFactory.customer_admin(), UserModelFactory.customer_admin()]
)
@pytest.mark.smoke
@allure.testcase('31554')
def test_report_can_be_resolved(
    user, api_request_context_addin, employee_reports_page, mailtrap
):
    message = 'Test Mail E2E Test ' + str(random.randint(100000000, 999999999))
    mail_content = b64encode(
        f"""From: Random Mail <random@mail.com>
Subject: {message}
Content-Type: multipart/alternative;
	boundary=mk3-e46c63ea11ba4304848685bb456f01b2; charset=UTF-8

--mk3-e46c63ea11ba4304848685bb456f01b2
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: quoted-printable

{message}
""".encode()
    ).decode('utf-8')
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.assessment(mail_content)
    expect(response).to_be_ok()

    assert 'id' in response.json()

    id = response.json()['id']
    Log.info(f'assessment lro id: {id}')
    last_status = wait_for_lro(
        lambda: assessment_service.assessment_report_by_id(id), 60
    )

    expect(last_status).to_be_ok()

    assert last_status.json()['status'] == 'DONE'
    employee_reports_page.last_report_column_header.click()
    employee_reports_page.last_report_column_header.click()
    reported_message = employee_reports_page.get_report(
        re.compile('.*' + message + '.*')
    )
    reported_message.get_by_role('button', name='Resolve').click()
    employee_reports_page.page.wait_for_load_state(timeout=5)

    expect(reported_message).to_have_count(0)


@pytest.mark.parametrize('user', [pytest.param(UserModelFactory.customer_admin())])
@allure.testcase('5846')
@pytest.mark.smoke
def test_assessment_outlook(user, outlook_page, mailtrap):
    # goto specific messagex
    outlook_page.open_addin()
    outlook_page.perform_assessment()
    expect(
        outlook_page.app_frame.get_by_text(
            'You’ve correctly reported a suspicious email'
        )
    ).to_be_visible(timeout=60 * 1000)
    outlook_page.close_gamification()
    mail = mailtrap.wait_for_mail(
        AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
        find_email(
            '68fa80bce3-28fbb0@inbox.mailtrap.io',
            'Security level Moderate-Low. Suspicious Email Report (Attachment included)',
        ),
        timeout=240,
    )
    assert mail is not None, (
        f'Unable to find email 68fa80bce3-28fbb0@inbox.mailtrap.io please check the mailtrap inbox {AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID}'
    )
    assert 'Suspicious Email Report' in mail['subject']
    outlook_page.provide_feedback()


@pytest.mark.parametrize('user', [pytest.param(UserModelFactory.customer_admin())])
@allure.testcase('5846')
@pytest.mark.smoke
def test_assessment_outlook_shared(user, outlook_page_shared, mailtrap):
    # goto specific messagex
    outlook_page_shared.open_addin()
    outlook_page_shared.perform_assessment()
    expect(
        outlook_page_shared.app_frame.get_by_text(
            'You’ve correctly reported a suspicious email'
        )
    ).to_be_visible(timeout=60 * 1000)
    outlook_page_shared.close_gamification()
    mail = mailtrap.wait_for_mail(
        AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
        find_email(
            '68fa80bce3-28fbb0@inbox.mailtrap.io',
            'Security level Moderate-Low. Suspicious Email Report (Attachment included)',
        ),
        timeout=240,
    )
    assert mail is not None, (
        f'Unable to find email 68fa80bce3-28fbb0@inbox.mailtrap.io please check the mailtrap inbox {AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID}'
    )
    assert 'Suspicious Email Report' in mail['subject']
    outlook_page_shared.provide_feedback()


@pytest.mark.parametrize('user', [pytest.param(UserModelFactory.customer_admin())])
@allure.testcase('5847')
@pytest.mark.smoke
def test_report_outlook(user, outlook_page, mailtrap):
    # goto specific message
    outlook_page.open_addin()
    outlook_page.report_incident()
    expect(
        outlook_page.app_frame.get_by_text('You’ve successfully reported an incident')
    ).to_be_visible(timeout=60 * 1000)
    outlook_page.close_gamification()
    mail = mailtrap.wait_for_mail(
        AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
        find_email(
            '68fa80bce3-28fbb0@inbox.mailtrap.io',
            'Incident Report (Attachment Included)',
        ),
        timeout=240,
    )
    assert mail is not None, (
        f'Unable to find email 68fa80bce3-28fbb0@inbox.mailtrap.io please check the mailtrap inbox {AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID}'
    )
    assert 'Incident Report' in mail['subject']


@pytest.mark.parametrize('user', [pytest.param(UserModelFactory.customer_admin())])
@allure.testcase('5847')
@pytest.mark.smoke
def test_report_outlook_shared(user, outlook_page_shared, mailtrap):
    # goto specific message
    outlook_page_shared.open_addin()
    outlook_page_shared.report_incident()
    expect(
        outlook_page_shared.app_frame.get_by_text(
            'You’ve successfully reported an incident'
        )
    ).to_be_visible(timeout=60 * 1000)
    outlook_page_shared.close_gamification()
    mail = mailtrap.wait_for_mail(
        AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
        find_email(
            '68fa80bce3-28fbb0@inbox.mailtrap.io',
            'Incident Report (Attachment Included)',
        ),
        timeout=240,
    )
    assert mail is not None, (
        f'Unable to find email 68fa80bce3-28fbb0@inbox.mailtrap.io please check the mailtrap inbox {AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID}'
    )
    assert 'Incident Report' in mail['subject']
