import allure
import pytest
from faker import Faker
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employee
from src.models.factories.company.employee_model_factory import EmployeeModelFactory

fake = Faker()


@allure.testcase('31563')
@pytest.mark.api
@pytest.mark.smoke
def test_upload_employees(api_request_context_customer_admin):
    employee = EmployeeModelFactory.get_random_employee()
    company = api.company(api_request_context_customer_admin)
    email = employee.email
    response = create_employee(api_request_context_customer_admin, employee)
    expect(response).to_be_ok()

    employee = company.employee_by_mail(email=email)

    assert employee['employee_role']
    assert not employee['admin_role']
    assert employee['email'] == email
