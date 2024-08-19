import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees_wait
from src.models.auth.user_model import UserModel
from src.models.company.employee_count_model import EmployeeCountModel
from src.models.company.employee_list_model import EmployeeItemModel, EmployeeListModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_item_model_factory import (
    EmployeeItemModelFactory,
)
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.page_objects.employee_directory import update_employee_success_message
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.page_objects.entity.employee_entity import EmployeeEntityFactory


@pytest.fixture(scope='function')
def get_employee(api_request_context_customer_admin_upload) -> EmployeeItemModel:
    company_service = api.company(api_request_context_customer_admin_upload)

    employees_list = EmployeeModelFactory.get_random_employees(1)
    create_employees_wait(
        api_request_context_customer_admin_upload, employees_list, overwrite=False
    )
    response = company_service.employee_count()
    expect(response).to_be_ok()
    employee_count_model = EmployeeCountModel.from_dict(response.json())
    response = company_service.get_employee_list(employee_count_model.employee_role)
    expect(response).to_be_ok()
    employee_list = EmployeeListModel.from_dict(response.json())
    return employee_list.items[0]


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user,employee_item',
    [
        pytest.param(
            UserModelFactory.customer_admin_upload(),
            EmployeeItemModelFactory.get_random_employee(),
            marks=pytest.mark.test_id('C31666'),
        )
    ],
)
def test_edit_employee_all_fields(
    get_employee,
    employee_directory_page: EmployeeDirectoryPage,
    user: UserModel,
    employee_item: EmployeeItemModel,
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
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin_upload(),
            marks=pytest.mark.test_id('C31667'),
        )
    ],
)
def test_deactivate_employee(
    get_employee, employee_directory_page: EmployeeDirectoryPage, user: UserModel
):
    employee_directory_page.deactivate_employee(email=get_employee.email)
