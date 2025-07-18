import allure
import pytest

from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.training_settings.group_settings_config import GroupSettingsConfig


@pytest.mark.parametrize(
    'user,settings',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            GroupSettingsConfig(
                edit_employees_feature=True,
                launch_campaigns_feature=False,
                read_campaigns_data_feature=False,
                resend_emails_feature=True,
                read_gamification_data_feature=False,
            ),
            id='Test Group Settings: Modify Group Settings',
            marks=[allure.testcase('31799'), pytest.mark.xdist_group('agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            GroupSettingsConfig(
                edit_employees_feature=True,
                launch_campaigns_feature=True,
                read_campaigns_data_feature=True,
                resend_emails_feature=True,
                read_gamification_data_feature=True,
            ),
            id='Test Group Settings: Modify Group Settings',
            marks=[allure.testcase('31799'), pytest.mark.xdist_group('agent1')],
        ),
    ],
)
def test_modify_group_settings(
    training_settings_group_settings_page, user, settings: GroupSettingsConfig
):
    training_settings_group_settings_page.modify_group_settings(settings)
