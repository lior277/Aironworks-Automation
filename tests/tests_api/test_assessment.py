import random
from typing import Generator
from src.utils.service_account_utils import generate_jwt
from src.configs.config_loader import AppConfigs
from src.apis.assessment import AssessmentService
from src.utils.waiter import wait_for_lro
from base64 import b64encode
from src.utils.mailtrap import find_attachment

import pytest
from playwright.sync_api import Playwright, APIRequestContext, expect
from src.utils.log import Log


@pytest.fixture(scope="session")
def example_mail():
    with open("tests/resources/example_mail.eml", "rb") as f:
        return f.read().replace(
            b"RANDOM_TEXT", str(random.randint(100000000, 999999999)).encode("utf-8")
        )


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.ADDIN_BASE_URL
    # Get service account email and load the json data from the service account key file.

    token = generate_jwt(
        AppConfigs.LOGIN_SA_ACCOUNT,
        audience=base_url,  # doesn't actually matter
    )
    headers = {"Authorization": "GG " + token}
    request_context = playwright.request.new_context(
        base_url=base_url, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


@pytest.mark.addin_api
def test_credentials_should_be_correct(api_request_context):
    response = AssessmentService.info(api_request_context)
    expect(response).to_be_ok()
    assert response.json() == {"soc_email": AppConfigs.MAILTRAP_ASSESSMENT_INBOX_MAIL}


@pytest.mark.addin_api
def test_assessment_api(api_request_context, example_mail, mailtrap):
    response = AssessmentService.assessment(
        api_request_context, b64encode(example_mail).decode("utf-8")
    )
    expect(response).to_be_ok()
    assert "id" in response.json()

    id = response.json()["id"]
    Log.info(f"assessment lro id: {id}")
    response = wait_for_lro(
        lambda: AssessmentService.assessment_by_id(api_request_context, id), 60
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


@pytest.mark.addin_api
def test_incident_report(api_request_context, example_mail, mailtrap):
    response = AssessmentService.incident(
        api_request_context, b64encode(example_mail).decode("utf-8")
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


@pytest.mark.addin_api
def test_assessment_report(api_request_context, mailtrap):
    message = "Test Mail E2E Test " + str(random.randint(100000000, 999999999))
    response = AssessmentService.assessment_report(
        api_request_context,
        message,
        "random@mail.com",
    )
    expect(response).to_be_ok()

    assert "id" in response.json()

    id = response.json()["id"]
    Log.info(f"assessment lro id: {id}")
    last_status = wait_for_lro(
        lambda: AssessmentService.assessment_report_by_id(api_request_context, id), 60
    )

    expect(last_status).to_be_ok()

    assert last_status.json()["status"] == "DONE"

    assert "assessment_result" in last_status.json()
    assessment_result = last_status.json()["assessment_result"]
    assert assessment_result["error"] is None
