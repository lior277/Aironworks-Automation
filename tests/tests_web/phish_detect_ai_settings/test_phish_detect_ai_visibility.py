import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.phish_detect_ui_settings.outlook_localized_config_factories import (
    OutlookLocalizedConfigFactory,
)
from src.models.phish_detect_ui_settings.outlook_localized_config import (
    OutlookConfigData,
)


@pytest.fixture(scope='function')
def set_outlook_default_setting(request, api_request_context_customer_admin):
    def finalizer():
        phish_detect_ui_service = api.phish_detect_ui_settings(
            api_request_context_customer_admin
        )
        expected_settings = OutlookLocalizedConfigFactory.get_default_en_config()
        response = phish_detect_ui_service.update_outlook_localized_config(
            expected_settings, language=expected_settings.language
        )
        expect(response).to_be_ok()
        actual_settings = OutlookConfigData.from_dict(response.json())
        assert expected_settings == actual_settings

    request.addfinalizer(finalizer)


@pytest.mark.parametrize(
    'user,settings',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            OutlookLocalizedConfigFactory.get_outlook_config(
                assessment_button=False,
                incident_button=True,
                completion_report_custom_text='Congratulations! You have successfully completed the assessment.',
            ),
            id='Test assessment_button visibility settings in phish detect ai',
            marks=[allure.testcase('31798'), pytest.mark.xdist_group('agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            OutlookLocalizedConfigFactory.get_outlook_config(
                assessment_button=True,
                incident_button=False,
                completion_report_custom_text='Congratulations! You have successfully completed the assessment.',
            ),
            id='Test incident_button visibility settings in phish detect ai',
            marks=[allure.testcase('31799'), pytest.mark.xdist_group('agent1')],
        ),
    ],
)
@pytest.mark.smoke
def test_phish_detect_ai_visibility_settings(
    phish_detect_ai_settings_configuration_page,
    user,
    set_outlook_default_setting,
    settings: OutlookConfigData,
):
    phish_detect_ai_settings_configuration_page.change_settings(settings)
    phish_detect_ai_settings_configuration_page.check_settings_in_preview(settings)
