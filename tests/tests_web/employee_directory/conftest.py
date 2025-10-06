from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees_wait
from src.configs.config_loader import AppConfigs
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.company.employee_list_model import EmployeeItemModel, EmployeeListModel
from src.models.company.employee_update_model import EmployeeUpdateModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_model_factory import EmployeeModelFactory


@pytest.fixture(scope='session')
def api_request_context_customer_admin_upload(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.BASE_URL
    # Get service account email and load the json data from the service account key file.

    request_context = playwright.request.new_context(base_url=base_url)
    login_service = api.login(request_context)
    expect(login_service.login(UserModelFactory.customer_admin_upload())).to_be_ok()
    login_info_response = login_service.info()
    expect(login_info_response).to_be_ok()
    login_info = login_info_response.json()
    assert 'user' in login_info
    assert 'roles' in login_info['user']
    assert len(login_info['user']['roles']) == 1
    role_id = login_info['user']['roles'][0]['id']
    expect(login_service.pick_role(role_id)).to_be_ok()
    yield request_context
    request_context.dispose()


@pytest.fixture(scope='session')
def clean_up_employees(request, api_request_context_customer_admin_upload):
    def finalizer():
        company_service = api.company(api_request_context_customer_admin_upload)
        response = company_service.get_employee_ids(
            EmployeeListIdsModel(employee_role=False, admin_role=False, filters=None)
        )
        expect(response).to_be_ok()
        if response.json()['items']:
            expect(
                company_service.delete_employees(
                    employees=EmployeeDeleteModel(ids=response.json()['items'])
                )
            ).to_be_ok()
        response = company_service.get_employee_ids(
            EmployeeListIdsModel(employee_role=True, admin_role=False, filters=None)
        )
        expect(response).to_be_ok()
        if response.json()['items']:
            expect(
                company_service.delete_employees(
                    employees=EmployeeDeleteModel(ids=response.json()['items'])
                )
            ).to_be_ok()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='function')
def get_employee(
    api_request_context_customer_admin, inactive: bool
) -> EmployeeItemModel:
    company_service = api.company(api_request_context_customer_admin)

    employee = EmployeeModelFactory.get_random_employees(1)
    create_employees_wait(api_request_context_customer_admin, employee, overwrite=False)
    response = company_service.employee_count()
    expect(response).to_be_ok()
    # employee_count_model = EmployeeCountModel.from_dict(response.json())
    filters = {
        'items': [
            {
                'columnField': 'email',
                'operatorValue': 'contains',
                'value': employee[0].email.lower(),
            }
        ],
        'linkOperator': 'and',
    }
    response = company_service.get_employee_list(50, filters)
    expect(response).to_be_ok()
    employee_list = EmployeeListModel.from_dict(response.json())
    employee_item = next(
        item
        for item in employee_list.items
        if item.email.lower() == employee[0].email.lower()
    )
    if inactive:
        company_service.update_employees(
            employees=EmployeeUpdateModel(employee_role=False, ids=[employee_item.id])
        )
    return employee_item
