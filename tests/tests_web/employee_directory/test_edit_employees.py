import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)

# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user,employee_item,inactive',
#     [
#         pytest.param(
#             UserModelFactory.customer_admin(),
#             EmployeeItemModelFactory.get_random_employee(),
#             False,
#             marks=allure.testcase('31666'),
#         )
#     ],
# )
# def test_edit_employee_all_fields(
#     get_employee,
#     employee_directory_page: EmployeeDirectoryPage,
#     user: UserModel,
#     employee_item: EmployeeItemModel,
#     inactive: bool,
# ):
#     expected_employee = EmployeeEntityFactory.from_employee_item(employee_item)
#     employee_directory_page.filter_employee_by_email(get_employee.email)
#     employee_directory_page.edit_employee(employee_item)
#     employee_directory_page.ensure_alert_message_is_visible(
#         update_employee_success_message
#     )
#     actual_employee = employee_directory_page.get_employee_entity_by_email(
#         employee_item.email
#     )
#     assert expected_employee == actual_employee, (
#         f'{expected_employee=}\n\n{actual_employee=}'
#     )


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,inactive',
    [
        pytest.param(
            UserModelFactory.customer_admin(), False, marks=allure.testcase('31667')
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
            UserModelFactory.customer_admin(), True, marks=allure.testcase('30815')
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


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,inactive',
    [
        pytest.param(
            UserModelFactory.customer_admin(), True, marks=allure.testcase('31668')
        )
    ],
)
def test_delete_employee(
    get_employee,
    employee_directory_page: EmployeeDirectoryPage,
    user: UserModel,
    inactive: bool,
):
    employee_directory_page.delete_employee(email=get_employee.email)
