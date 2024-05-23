import pytest
from faker import Faker
from playwright.sync_api import expect

from src.apis.company import CompanyService
from src.models.factories.company.employee_model_factory import EmployeeModelFactory

fake = Faker()


@pytest.mark.test_id("C31563")
@pytest.mark.api
@pytest.mark.smoke
def test_upload_employees(api_request_context_customer_admin):
    employee = EmployeeModelFactory.get_random_employee()
    email = employee.email
    response = CompanyService.create_employee(api_request_context_customer_admin, employee)
    expect(response).to_be_ok()

    employee = CompanyService.employee_by_mail(api_request_context_customer_admin, email=email)
    assert employee["employee_role"]
    assert not employee["admin_role"]
    assert employee["email"] == email
