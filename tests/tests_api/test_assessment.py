from base64 import b64encode

import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.models.addin.assessment_info_model import AssessmentInfoModel
from src.models.factories.adding.assessment_info_model_factory import (
    AssessmentInfoModelFactory,
)
from src.utils.log import Log
from src.utils.waiter import wait_for_lro


@allure.testcase('31557')
@pytest.mark.addin_api
def test_credentials_should_be_correct(api_request_context_addin):
    expected_assessment_info = AssessmentInfoModelFactory.get_default_info(
        AppConfigs.MAILTRAP_ASSESSMENT_INBOX_MAIL
    )
    assessment_service = api.assessment(api_request_context_addin)

    response = assessment_service.info()
    expect(response).to_be_ok()
    actual_assessment_info = AssessmentInfoModel.from_dict(response.json())

    assert expected_assessment_info == actual_assessment_info, (
        f'{expected_assessment_info=}\n\n{actual_assessment_info=}'
    )


@allure.testcase('31558')
@pytest.mark.addin_api
def test_assessment_api(api_request_context_addin, example_mail, mailtrap):
    assessment_service = api.assessment(api_request_context_addin)
    response = assessment_service.assessment(b64encode(example_mail).decode('utf-8'))
    expect(response).to_be_ok()
    assert 'id' in response.json()

    assessment_lro_id = response.json()['id']
    Log.info(f'assessment lro id: {assessment_lro_id}')
    response = wait_for_lro(
        lambda: assessment_service.assessment_by_id(assessment_lro_id), 60
    )
    assert response.json()['status'] == 'DONE', response.json()['error']

    assert 'assessment_result' in response.json()
    assessment_result = response.json()['assessment_result']
    assert 'assessment' in assessment_result
    assert assessment_result['assessment']['error'] is None

    # assert (
    #     mailtrap.wait_for_mail(
    #         AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID, find_attachment()
    #     )
    #     is not None
    # )
