from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright, expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.factories.auth.user_model_factory import UserModelFactory


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


@pytest.fixture(scope='session', autouse=True)
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
