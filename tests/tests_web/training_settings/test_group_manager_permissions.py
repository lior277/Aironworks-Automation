import allure
import pytest

from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.training_settings.group_manager_permissions_config import (
    GroupManagerPermissionsConfig,
)


@pytest.mark.parametrize(
    'user,settings',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            GroupManagerPermissionsConfig(
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
            GroupManagerPermissionsConfig(
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
def test_modify_group_manager_permissions(
    training_settings_group_manager_permissions_page,
    user,
    settings: GroupManagerPermissionsConfig,
):
    training_settings_group_manager_permissions_page.test_modify_group_manager_permissions(
        settings
    )
