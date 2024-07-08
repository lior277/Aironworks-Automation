import os

import pytest

from src.apis.api_factory import api
from src.apis.scenario import ScenarioService
from src.apis.steps.common_steps import create_employees_wait
from src.apis.survey_service import SurveyService
from src.configs.config_loader import AppFolders
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_assignments import EducationAssignmentsModel
from src.models.education.education_content_model import EducationContentModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import (
    EducationCampaignModelFactory,
)
from src.models.factories.scenario.campaign_model_factory import CampaignModelFactory
from src.models.factories.scenario.list_attack_infos_model_factory import (
    ListAttackInfosModelFactory,
)
from src.models.general_models import LongRunningOperation
from src.models.mait_trap_model import MailTrapModelFactory
from src.models.scenario.list_attack_infos_response_model import (
    ListAttackInfosResponseModel,
)
from src.models.survey.get_survey import GetSurveyModel
from src.models.survey.surveys_model import Survey
from src.utils.csv_tool import CSVTool


@pytest.mark.parametrize("employees_count", [2])
def test_education_campaign(api_request_context_customer_admin, api_request_context_aw_admin, employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count, domain="aironworks.com")
    company = api.company(api_request_context_customer_admin)
    education = api.education(api_request_context_customer_admin)
    response = company.create_employees(employees_list, overwrite=True)
    response_body = LongRunningOperation.from_dict(response.json())
    assert response.ok, f"Failed to upload file with employee. Response => {response_body}"

    response = company.get_employee_ids(EmployeeListIdsModel(employee_role=True, filters=None))
    employee_ids = response.json()
    assert (
            len(employee_ids["items"]) == employees_count
    ), f"Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}"

    response = education.get_content_pagination()
    assert response.ok, f"Failed to fetch education content => {response.json()}"
    education_content = EducationContentModel.from_dict(response.json())
    education_campaign = (
        EducationCampaignModelFactory.get_education_campaign_from_education_content(
            education_content.items[0], employee_ids["items"]
        )
    )
    response = education.start_campaign(education_campaign)
    assert response.ok, f"Failed to start education campaign => {response_body}"
    response = api.education(api_request_context_aw_admin).aw_admin_education_assignments(
        campaign_id=response.json()["id"])
    education_assignments = EducationAssignmentsModel.from_dict(response.json())
    file_path = os.path.join(AppFolders.RESOURCES_PATH, "perf_education_campaign.csv")
    fieldnames = education_assignments.assignments[0].get_fieldnames()
    CSVTool.create_file(education_assignments.assignments, fieldnames, file_path)


@pytest.mark.parametrize("employees_count", [1])
def test_generate_employees(employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(
        employees_count,
        mailtrap_inbox=MailTrapModelFactory.get_perf_mail_trap_inbox().email,
    )

    file_path = os.path.join(
        AppFolders.RESOURCES_PATH, f"employees{employees_count}.csv"
    )
    column_names = ["First Name", "Last Name", "Email"]
    CSVTool.create_file(employees_list, column_names, file_path)


@pytest.mark.parametrize("employees_count", [1000])
@pytest.mark.timeout(60 * 60)
def test_simulation_campaign(api_request_context_customer_admin, clean_up_employees, set_up_perf_survey: Survey,
                             api_request_context_aw_admin, employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count, domain="aironworks.com")
    company = api.company(api_request_context_customer_admin)
    login_service = api.login(api_request_context_customer_admin)
    response = create_employees_wait(api_request_context_customer_admin, employees_list, overwrite=True)
    assert response.ok, f"{response.json()}"

    response = company.get_employee_ids(EmployeeListIdsModel(employee_role=True, filters=None))
    employee_ids = response.json()
    assert (
            len(employee_ids["items"]) == employees_count
    ), f"Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}"

    response = ScenarioService.post_list_attack_infos(
        api_request_context_customer_admin,
        ListAttackInfosModelFactory.get_list_attack_infos(),
    )
    list_attack_infos = ListAttackInfosResponseModel.from_dict(response.json())
    assert len(list_attack_infos.infos) > 0
    infos = list_attack_infos.infos[0]
    response = login_service.info()
    campaign_model = CampaignModelFactory.get_campaign(
        campaign_name=infos.strategy_name,
        company_id=response.json()["user"]["company_id"],
        employees=employee_ids["items"],
        attack_info_id=infos.id,
    )
    admin_service = api.admin(api_request_context_customer_admin)
    response = admin_service.start_campaign(campaign_model)

    campaign_urls = ScenarioService.aw_admin_campaign_urls(
        api_request_context_aw_admin, campaign_id=response.json()["id"]
    )
    file_path = os.path.join(AppFolders.RESOURCES_PATH, "perf_warning_page.csv")
    fieldnames = campaign_urls.attacks[0].get_fieldnames()
    response = SurveyService.get_survey(
        api_request_context_customer_admin, set_up_perf_survey.id
    )
    assert response.ok, f"{response.json()=}"
    survey = GetSurveyModel.from_dict(response.json())
    fieldnames.extend(["qid", "option_id", "survey_id"])
    data_to_update = {
        "qid": f"{survey.model.questions[0].id}",
        "option_id": f"{survey.model.questions[0].options[0].id}",
        "survey_id": f"{survey.model.id}",
    }
    CSVTool.create_file(campaign_urls.attacks, fieldnames, file_path, data_to_update)
