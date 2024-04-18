from playwright.sync_api import expect
from src.apis.company import CompanyService
from faker import Faker

fake = Faker()


def test_upload_employees(api_request_context_customer_admin):
    response = CompanyService.create_employee(
        api_request_context_customer_admin,
        fake.email(),
        fake.first_name(),
        fake.last_name(),
    )
    expect(response).to_be_ok()
