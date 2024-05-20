import pytest
import random
from src.utils.mailtrap import MailTrap
from src.configs.config_loader import AppConfigs
from playwright.sync_api import Playwright, APIRequestContext, expect
from typing import Generator
from src.utils.service_account_utils import generate_jwt
from src.models.factories.user_model_factory import UserModelFactory
from src.models.employee_model import EmployeeModel
from src.apis.login import LoginService
from src.apis.company import CompanyService
from dataclasses import replace
from faker import Faker

fake = Faker()


@pytest.fixture(scope="session")
def mailtrap(playwright):
    mailtrap = MailTrap(playwright)
    yield mailtrap
    mailtrap.close()


@pytest.fixture(scope="session")
def example_mail():
    with open("tests/resources/example_mail.eml", "rb") as f:
        return f.read().replace(
            b"RANDOM_TEXT", str(random.randint(100000000, 999999999)).encode("utf-8")
        )


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))


@pytest.fixture(scope="session")
def api_request_context_addin(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.ADDIN_BASE_URL
    # Get service account email and load the json data from the service account key file.

    token = generate_jwt(
        AppConfigs.LOGIN_SA_ACCOUNT,
        audience=base_url,  # doesn't actually matter
    )
    headers = {"Authorization": "GG " + token}
    request_context = playwright.request.new_context(
        base_url=base_url, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def api_request_context_customer_admin(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.BASE_URL
    # Get service account email and load the json data from the service account key file.

    request_context = playwright.request.new_context(base_url=base_url)
    expect(
        LoginService.login(request_context, UserModelFactory.customer_admin())
    ).to_be_ok()
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
    employee = EmployeeModel(None, email, fake.first_name(), fake.last_name())
    response = CompanyService.create_employee(
        api_request_context_customer_admin, employee
    )
    expect(response).to_be_ok()

    employee_data = CompanyService.employee_by_mail(
        api_request_context_customer_admin, email=email
    )

    assert employee_data["employee_role"]
    assert not employee_data["admin_role"]
    assert employee_data["email"] == email

    return replace(employee, employee_id=employee_data["id"])
