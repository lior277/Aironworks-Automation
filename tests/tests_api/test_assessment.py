import random
from base64 import b64encode

import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.utils.log import Log
from src.utils.mailtrap import find_attachment
from src.utils.waiter import wait_for_lro


@pytest.mark.test_id("C31557")
@pytest.mark.addin_api
def test_credentials_should_be_correct(api_request_context_addin):
    assessment_service = api.assessment(api_request_context_addin)

    response = assessment_service.info()
    expect(response).to_be_ok()
    assert response.json() == {"soc_email": AppConfigs.MAILTRAP_ASSESSMENT_INBOX_MAIL}


@pytest.mark.test_id("C31558")
@pytest.mark.addin_api
def test_assessment_api(api_request_context_addin, example_mail, mailtrap):
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.assessment(b64encode(example_mail).decode("utf-8"))
    expect(response).to_be_ok()
    assert "id" in response.json()

    assessment_lro_id = response.json()["id"]
    Log.info(f"assessment lro id: {assessment_lro_id}")
    response = wait_for_lro(lambda: assessment_service.assessment_by_id(assessment_lro_id), 60)
    assert response.json()["status"] == "DONE", response.json()["error"]

    assert "assessment_result" in response.json()
    assessment_result = response.json()["assessment_result"]
    assert "assessment" in assessment_result
    assert "forward" in assessment_result
    assert assessment_result["forward"] == {"error": None}
    assert assessment_result["assessment"]["error"] is None

    assert mailtrap.wait_for_mail(AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID, find_attachment()) is not None


@pytest.mark.test_id("C31559")
@pytest.mark.addin_api
def test_incident_report(api_request_context_addin, example_mail, mailtrap):
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.incident(b64encode(example_mail).decode("utf-8"))
    expect(response).to_be_ok()

    assert response.json()["error"] is None

    assert mailtrap.wait_for_mail(AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID, find_attachment()) is not None


@pytest.mark.test_id("C31560")
@pytest.mark.addin_api
def test_assessment_report(api_request_context_addin, mailtrap):
    message = "Test Mail E2E Test " + str(random.randint(100000000, 999999999))
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.assessment_report(message, "random@mail.com", )
    expect(response).to_be_ok()

    assert "id" in response.json()

    assessment_lro_id = response.json()["id"]
    Log.info(f"assessment lro id: {assessment_lro_id}")
    last_status = wait_for_lro(lambda: assessment_service.assessment_report_by_id(assessment_lro_id), 60)

    expect(last_status).to_be_ok()

    assert last_status.json()["status"] == "DONE"

    assert "assessment_result" in last_status.json()
    assessment_result = last_status.json()["assessment_result"]
    assert assessment_result["error"] is None
