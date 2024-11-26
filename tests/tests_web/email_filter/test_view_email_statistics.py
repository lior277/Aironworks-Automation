import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            marks=allure.testcase('C31803'),
        )
    ],
)
def test_view_email_statistics(
    is_emailfilter_enabled, email_statistics_page, user: UserModel
):
    email_statistics_page.verify_sections_display()
