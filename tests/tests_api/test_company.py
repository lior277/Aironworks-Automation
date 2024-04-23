from playwright.sync_api import expect
from src.apis.psapi import PSApi
from faker import Faker

fake = Faker()


def test_upload_employees(api_request_context_customer_admin):
    email = fake.email()
    response = PSApi.create_employee(
        api_request_context_customer_admin,
        email,
        fake.first_name(),
        fake.last_name(),
    )
    expect(response).to_be_ok()

    employee = PSApi.employee_by_mail(api_request_context_customer_admin, email=email)
    assert employee["employee_role"]
    assert not employee["admin_role"]
    assert employee["email"] == email
