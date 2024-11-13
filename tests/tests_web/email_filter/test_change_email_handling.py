import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, option',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'Block High-Risk Email',
            marks=allure.testcase('C31803'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'Label As High-Risk Only',
            marks=allure.testcase('C31804'),
        ),
    ],
)
def test_change_email_handling(
    user: UserModel, email_filter_settings_page, option, is_emailfilter_enabled
):
    email_filter_settings_page.update_high_risk_emails_handling(option)
