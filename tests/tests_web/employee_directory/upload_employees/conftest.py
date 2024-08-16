import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel


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
