import pytest
from playwright.sync_api import expect

from src.models.auth.user_model import UserModel
from src.models.company.employee_list_model import EmployeeItemModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_item_model_factory import (
    EmployeeItemModelFactory,
)
from src.page_objects.employee_directory import update_employee_success_message
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.page_objects.entity.employee_entity import EmployeeEntityFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,employee_item,inactive',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            EmployeeItemModelFactory.get_random_employee(),
            False,
            marks=pytest.mark.test_id('C31666'),
        )
    ],
)
def test_edit_employee_all_fields(
    get_employee,
    employee_directory_page: EmployeeDirectoryPage,
    user: UserModel,
    employee_item: EmployeeItemModel,
    inactive: bool,
):
    expected_employee = EmployeeEntityFactory.from_employee_item(employee_item)
    employee_directory_page.filter_employee_by_email(get_employee.email)
    employee_directory_page.edit_employee(employee_item)
    expect(employee_directory_page.alert_message).to_have_text(
        update_employee_success_message
    )
    actual_employee = employee_directory_page.get_employee_entity_by_email(
        employee_item.email
    )
    assert (
        expected_employee == actual_employee
    ), f'{expected_employee=}\n\n{actual_employee=}'


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,inactive',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            False,
            marks=pytest.mark.test_id('C31667'),
        )
    ],
)
def test_deactivate_employee(
    get_employee,
    employee_directory_page: EmployeeDirectoryPage,
    user: UserModel,
    inactive: bool,
):
    employee_directory_page.deactivate_employee(email=get_employee.email)


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,inactive',
    [
        pytest.param(
            UserModelFactory.customer_admin(), True, marks=pytest.mark.test_id('C30815')
        )
    ],
)
def test_restore_employee(
    get_employee,
    employee_directory_page: EmployeeDirectoryPage,
    user: UserModel,
    inactive: bool,
):
    employee_directory_page.restore_employee(email=get_employee.email)
