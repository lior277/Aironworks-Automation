import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.operation.operation_model_factory import OperationModelFactory
from src.models.operation_model import OperationModel


@pytest.mark.parametrize(
    'user, operation',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            OperationModelFactory.get_operation(),
            marks=allure.testcase('31798'),
        )
    ],
)
@pytest.mark.smoke
def test_create_operation(
    user: UserModel, operation: OperationModel, operations_list_page
):
    create_operation_page = operations_list_page.navigate_to_create_operation_page()
    create_operation_page.create_operation(operation)
