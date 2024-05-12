import random
from src.configs.config_loader import AppConfigs
from src.apis.assessment import AssessmentService
from src.utils.waiter import wait_for_lro
from base64 import b64encode
from src.utils.mailtrap import find_attachment
from playwright.sync_api import expect

import pytest
from src.utils.log import Log


@pytest.mark.test_id("C31557")
@pytest.mark.addin_api
def test_credentials_should_be_correct(api_request_context_addin):
    response = AssessmentService.info(api_request_context_addin)
    expect(response).to_be_ok()
    assert response.json() == {"soc_email": AppConfigs.MAILTRAP_ASSESSMENT_INBOX_MAIL}


@pytest.mark.test_id("C31558")
@pytest.mark.addin_api
def test_assessment_api(api_request_context_addin, example_mail, mailtrap):
    response = AssessmentService.assessment(
        api_request_context_addin, b64encode(example_mail).decode("utf-8")
    )
    expect(response).to_be_ok()
    assert "id" in response.json()

    id = response.json()["id"]
    Log.info(f"assessment lro id: {id}")
    response = wait_for_lro(
        lambda: AssessmentService.assessment_by_id(api_request_context_addin, id), 60
    )
    assert response.json()["status"] == "DONE"

    assert "assessment_result" in response.json()
    assessment_result = response.json()["assessment_result"]
    assert "assessment" in assessment_result
    assert "forward" in assessment_result
    assert assessment_result["forward"] == {"error": None}
    assert assessment_result["assessment"]["error"] is None

    assert (
        mailtrap.wait_for_mail(
            AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
            find_attachment(example_mail),
        )
        is not None
    )


@pytest.mark.test_id("C31559")
@pytest.mark.addin_api
def test_incident_report(api_request_context_addin, example_mail, mailtrap):
    response = AssessmentService.incident(
        api_request_context_addin, b64encode(example_mail).decode("utf-8")
    )
    expect(response).to_be_ok()

    assert response.json()["error"] is None

    assert (
        mailtrap.wait_for_mail(
            AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID,
            find_attachment(example_mail),
        )
        is not None
    )


@pytest.mark.test_id("C31560")
@pytest.mark.addin_api
def test_assessment_report(api_request_context_addin, mailtrap):
    message = "Test Mail E2E Test " + str(random.randint(100000000, 999999999))
    response = AssessmentService.assessment_report(
        api_request_context_addin,
        message,
        "random@mail.com",
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

    assert "assessment_result" in last_status.json()
    assessment_result = last_status.json()["assessment_result"]
    assert assessment_result["error"] is None
