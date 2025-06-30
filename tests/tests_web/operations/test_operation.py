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
            marks=[allure.testcase('31798'), pytest.mark.xdist_group(name='agent1')],
        )
    ],
)
@pytest.mark.smoke
def test_create_operation(
    user: UserModel, operation: OperationModel, operations_list_page
):
    create_operation_page = operations_list_page.navigate_to_create_operation_page()
    create_operation_page.create_operation(operation)


@pytest.mark.parametrize(
    'user, operation',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            OperationModelFactory.get_operation_edit(),
            marks=[allure.testcase('31798'), pytest.mark.xdist_group(name='agent1')],
        )
    ],
)
@pytest.mark.smoke
def test_edit_operation(
    user: UserModel, operation: OperationModel, operations_list_page
):
    operation_detail_page = operations_list_page.navigate_to_first_operation_page()
    edit_operation_page = operation_detail_page.navigate_to_edit_operation_page()
    edit_operation_page.edit_operation(operation)


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            marks=[allure.testcase('31798'), pytest.mark.xdist_group(name='agent1')],
        )
    ],
)
@pytest.mark.smoke
def test_delete_operation(user: UserModel, operations_list_page):
    create_operation_page = operations_list_page.navigate_to_first_operation_page()
    create_operation_page.delete_operation()
