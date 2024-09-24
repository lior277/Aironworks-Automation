import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees_wait
from src.models.company.employee_list_model import EmployeeListModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.group.add_group import AddGroupModel
from src.models.group.group_list import GroupDetailsModel
from src.utils.randomizer import generate_string


@pytest.fixture(scope='function')
def get_group_managers_and_employees(api_request_context_customer_admin):
    company_service = api.company(api_request_context_customer_admin)

    employees = EmployeeModelFactory.get_random_employees(2)
    create_employees_wait(
        api_request_context_customer_admin, employees, overwrite=False
    )
    response = company_service.get_employee_list(
        1,
        filters={
            'items': [
                {
                    'columnField': 'email',
                    'operatorValue': 'contains',
                    'id': 0,
                    'value': employees[0].email.lower(),
                }
            ],
            'linkOperator': 'and',
            'quickFilterValues': [],
            'quickFilterLogicOperator': 'and',
        },
    )
    expect(response).to_be_ok()
    employee_list = EmployeeListModel.from_dict(response.json())
    employee_item = next(
        item
        for item in employee_list.items
        if item.email.lower() == employees[0].email.lower()
    )
    response = company_service.get_employee_list(
        1,
        filters={
            'items': [
                {
                    'columnField': 'email',
                    'operatorValue': 'contains',
                    'id': 0,
                    'value': employees[1].email.lower(),
                }
            ],
            'linkOperator': 'and',
            'quickFilterValues': [],
            'quickFilterLogicOperator': 'and',
        },
    )
    expect(response).to_be_ok()
    employee_list = EmployeeListModel.from_dict(response.json())
    manager_item = next(
        item
        for item in employee_list.items
        if item.email.lower() == employees[1].email.lower()
    )

    return manager_item, employee_item


@pytest.fixture(scope='function')
def create_group(api_request_context_customer_admin, get_group_managers_and_employees):
    manager = get_group_managers_and_employees[0]
    employee = get_group_managers_and_employees[1]
    add_group_model = AddGroupModel(
        name=generate_string(), employee_ids=[employee.id], manager_ids=[manager.id]
    )
    group_service = api.group(api_request_context_customer_admin)
    response = group_service.add_group(add_group_model)
    expect(response).to_be_ok()
    group_id = response.json()['id']
    response = group_service.get_group(group_id)
    expect(response).to_be_ok()
    group = GroupDetailsModel.from_dict(response.json())
    return group


@pytest.fixture(scope='function')
def delete_group(request, api_request_context_customer_admin, create_group):
    group_service = api.group(api_request_context_customer_admin)

    def finalizer():
        response = group_service.delete_group(create_group.group.id)
        expect(response).to_be_ok()

    request.addfinalizer(finalizer)
    return create_group
