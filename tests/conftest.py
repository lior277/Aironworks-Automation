import random
from dataclasses import replace
from typing import Generator

import pytest
from faker import Faker
from playwright.sync_api import Playwright, APIRequestContext, expect

from src.apis.company import CompanyService
from src.apis.login import LoginService
from src.apis.survey_service import SurveyService
from src.configs.config_loader import AppConfigs
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.company.employee_model import EmployeeModel
from src.models.company.employee_update_model import EmployeeUpdateModel
from src.models.company.localized_configs_model import LocalizedConfigsModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.patch_localized_configs_model import PatchLocalizedConfigsModelFactory
from src.models.factories.survey.add_survey_modal_factory import AddSurveyModelFactory
from src.models.survey.surveys_model import SurveysModel
from src.utils.list import divide_list_into_chunks
from src.utils.mailtrap import MailTrap
from src.utils.service_account_utils import generate_jwt

fake = Faker()


@pytest.fixture(scope="function")
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
        if item.get_closest_marker("timeout") is None:
            item.add_marker(pytest.mark.timeout(3 * 60))

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
    employee = EmployeeModel(
        email, fake.first_name(), fake.last_name(), employee_id=None
    )
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


@pytest.fixture(scope="session")
def api_request_context_aw_admin(
        playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=AppConfigs.ADMIN_BASE_URL)
    expect(LoginService.login(request_context, UserModelFactory.aw_admin())).to_be_ok()
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


@pytest.fixture(scope="function")
def clean_up_employees(api_request_context_customer_admin):
    response = CompanyService.get_employee_ids(
        api_request_context_customer_admin,
        EmployeeListIdsModel(employee_role=True, admin_role=False, filters=None),
    )
    if response.json()["items"]:
        CompanyService.update_employees(
            api_request_context_customer_admin,
            employees=EmployeeUpdateModel(
                employee_role=False, ids=list(response.json()["items"])
            ),
        )
    response = CompanyService.get_employee_ids(
        api_request_context_customer_admin,
        EmployeeListIdsModel(employee_role=False, admin_role=False, filters=None),
    )
    if response.json()["items"]:
        divided_list = divide_list_into_chunks(response.json()["items"], 2000)
        for chunk in divided_list:
            CompanyService.delete_employees(
                api_request_context_customer_admin,
                employees=EmployeeDeleteModel(ids=chunk),
            )


@pytest.fixture(scope="function")
def set_up_ca_settings(api_request_context_customer_admin):
    perf_survey = AddSurveyModelFactory.get_performance_survey()
    localized_config_response = CompanyService.localized_config(api_request_context_customer_admin)
    assert localized_config_response.ok, f"{localized_config_response.json()=}"
    data = LocalizedConfigsModel.from_dict(localized_config_response.json()).data[0]
    patch_localized_configs = PatchLocalizedConfigsModelFactory.get_patch_localized_configs(data)
    patch_localized_configs.show_survey_button = True
    response = CompanyService.patch_localized_config(api_request_context_customer_admin,
                                                     language=data.language,
                                                     localized_configs_model=patch_localized_configs)
    assert response.ok, f"{response.json()=}"
    response = SurveyService.get_list_surveys(api_request_context_customer_admin)
    assert response.ok, f"{response.json()=}"
    surveys_model = SurveysModel.from_dict(response.json())
    survey = surveys_model.has_survey(perf_survey.survey_name)
    if not survey:
        response = SurveyService.add_survey(api_request_context_customer_admin, perf_survey)
        assert response.ok, f"{response.json()=}"
        response = SurveyService.get_list_surveys(api_request_context_customer_admin)
        assert response.ok, f"{response.json()=}"
        surveys_model = SurveysModel.from_dict(response.json())
        survey = surveys_model.has_survey(perf_survey.survey_name)
    if not survey.always_sent:
        SurveyService.set_default_survey(api_request_context_customer_admin, survey.id)
