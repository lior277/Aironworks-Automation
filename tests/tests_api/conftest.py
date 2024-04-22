import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext, expect
from src.configs.config_loader import AppConfigs
from src.models.factories.user_model_factory import UserModelFactory
from src.models.employee_model import EmployeeModel
from src.apis.login import LoginService
from src.apis.company import CompanyService
from faker import Faker

fake = Faker()


@pytest.fixture(scope="session")
def api_request_context_customer_admin(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.BASE_URL
    # Get service account email and load the json data from the service account key file.

    request_context = playwright.request.new_context(base_url=base_url)
    expect(LoginService.login(request_context, UserModelFactory.my_user())).to_be_ok()
    login_info_response = LoginService.info(request_context)
    expect(login_info_response).to_be_ok()
    login_info = login_info_response.json()
    assert "user" in login_info
    assert "roles" in login_info["user"]
    assert len(login_info["user"]["roles"]) == 1
    role_id = login_info["user"]["roles"][0]["id"]
    expect(LoginService.pick_role(request_context, role_id)).to_be_ok()
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.BASE_URL
    # Get service account email and load the json data from the service account key file.

    request_context = playwright.request.new_context(base_url=base_url)

    yield request_context

    request_context.dispose()


@pytest.fixture(scope="function")
def employee(api_request_context_customer_admin):
    email = AppConfigs.EMPLOYEE_INBOX % fake.pystr().lower()
    print(email)
    response = CompanyService.create_employee(
        api_request_context_customer_admin,
        email,
        fake.first_name(),
        fake.last_name(),
    )
    expect(response).to_be_ok()

    employee = CompanyService.employee_by_mail(
        api_request_context_customer_admin, email=email
    )

    assert employee["employee_role"]
    assert not employee["admin_role"]
    assert employee["email"] == email

    return EmployeeModel(employee_id=employee["id"], email=employee["email"])
