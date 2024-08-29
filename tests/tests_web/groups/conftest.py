import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees_wait
from src.models.company.employee_count_model import EmployeeCountModel
from src.models.company.employee_list_model import EmployeeListModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory


@pytest.fixture(scope='function')
def get_group_managers_and_employees(api_request_context_customer_admin):
    company_service = api.company(api_request_context_customer_admin)

    employees = EmployeeModelFactory.get_random_employees(2)
    create_employees_wait(
        api_request_context_customer_admin, employees, overwrite=False
    )
    response = company_service.employee_count()
    expect(response).to_be_ok()
    employee_count_model = EmployeeCountModel.from_dict(response.json())
    response = company_service.get_employee_list(employee_count_model.employee_role)
    expect(response).to_be_ok()
    employee_list = EmployeeListModel.from_dict(response.json())
    employee_item = next(
        item
        for item in employee_list.items
        if item.email.lower() == employees[0].email.lower()
    )
    manager_item = next(
        item
        for item in employee_list.items
        if item.email.lower() == employees[1].email.lower()
    )

    return manager_item, employee_item
