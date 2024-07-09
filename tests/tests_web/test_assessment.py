import random
import re

import pytest
from playwright.sync_api import expect

from src.apis.assessment import AssessmentService
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.utils.log import Log
from src.utils.waiter import wait_for_lro


@pytest.mark.parametrize("user", [UserModelFactory.customer_admin()])
@pytest.mark.smoke
def test_report_can_be_resolved(user, api_request_context_addin, employee_reports_page):
    message = "Test Mail E2E Test " + str(random.randint(100000000, 999999999))
    response = AssessmentService.assessment_report(
        api_request_context_addin, message, "random@mail.com", subject=message
    )
    expect(response).to_be_ok()

    assert "id" in response.json()

    id = response.json()["id"]
    Log.info(f"assessment lro id: {id}")
    last_status = wait_for_lro(
        lambda: AssessmentService.assessment_report_by_id(
            api_request_context_addin, id
        ),
        60,
    )

    expect(last_status).to_be_ok()

    assert last_status.json()["status"] == "DONE"

    employee_reports_page.last_report_column_header.click()
    employee_reports_page.last_report_column_header.click()
    reported_message = employee_reports_page.get_report(re.compile(".*" + message + ".*"))
    reported_message.get_by_role("button", name="Resolve").click()
    employee_reports_page.page.wait_for_load_state(timeout=5)

    expect(reported_message).to_have_count(0)
