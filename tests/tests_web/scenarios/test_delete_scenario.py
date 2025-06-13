import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.scenarios_page import ScenariosPage


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            id='test create scenario customer admin',
            marks=allure.testcase('31490'),
        )
    ],
)
@pytest.mark.smoke
def test_create_scenario(user: UserModel, scenarios_page: ScenariosPage):
    scenarios_page.delete_scenario()
