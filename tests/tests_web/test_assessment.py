import random
import re

import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.utils.log import Log
from src.utils.waiter import wait_for_lro


@pytest.mark.parametrize('user', [UserModelFactory.customer_admin()])
@pytest.mark.smoke
@allure.testcase('31554')
def test_report_can_be_resolved(user, api_request_context_addin, employee_reports_page):
    message = 'Test Mail E2E Test ' + str(random.randint(100000000, 999999999))
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.assessment_report(
        message, 'random@mail.com', subject=message
    )
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


@allure.testcase('5846')
@pytest.mark.smoke
def test_assessment_outlook(outlook_page):
    # goto specific message
    outlook_page.goto_message(
        'AAQkADU4NWIwYzE0LTE2YzgtNGU0Yy04MWQ0LTg0ZmM3Y2NkNzg3OQAQAOkzkoNssJVOi%2FlzAm9aLr0%3D'
    )
    outlook_page.open_addin()
    outlook_page.perform_assessment()
    expect(
        outlook_page.app_frame.get_by_text('The email was sent to your')
    ).to_be_visible(timeout=60 * 1000)
