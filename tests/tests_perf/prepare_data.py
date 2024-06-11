import os

import pytest

from src.apis.admin import AdminService
from src.apis.company import CompanyService
from src.apis.education import EducationService
from src.apis.login import LoginService
from src.apis.scenario import ScenarioService
from src.configs.config_loader import AppFolders
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_assignments import EducationAssignmentsModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import EducationCampaignModelFactory
from src.models.factories.scenario.campaign_model_factory import CampaignModelFactory
from src.models.factories.scenario.list_attack_infos_model_factory import ListAttackInfosModelFactory
from src.models.general_models import BasicModel
from src.models.scenario.list_attack_infos_response_model import ListAttackInfosResponseModel
from src.utils.csv_tool import CSVTool


@pytest.mark.parametrize("employees_count", [1000])
def test_education_campaign(api_request_context_customer_admin, api_request_context_aw_admin, employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count, domain="aironworks.com")
    response = CompanyService.create_employees(api_request_context_customer_admin, employees_list, overwrite=True)
    response_body = BasicModel.from_dict(response.json())
    assert response_body.data.success and response.ok, f"Failed to upload file with employee. Response => {response_body}"

    response = CompanyService.get_employee_ids(api_request_context_customer_admin,
                                               EmployeeListIdsModel(employee_role=True, filters=None))
    employee_ids = response.json()
    assert len(employee_ids["items"]) == employees_count, \
        f"Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}"
    education_campaign = EducationCampaignModelFactory.get_education_campaign(employee_ids["items"])
    response = EducationService.start_campaign(api_request_context_customer_admin, education_campaign)
    response = EducationService.aw_admin_education_assignments(api_request_context_aw_admin,
                                                               campaign_id=response.json()['id'])
    education_assignments = EducationAssignmentsModel.from_dict(response.json())
    file_path = os.path.join(AppFolders.RESOURCES_PATH, "perf_education_campaign.csv")
    fieldnames = education_assignments.assignments[0].get_fieldnames()
    CSVTool.create_file(education_assignments.assignments, fieldnames, file_path)


@pytest.mark.parametrize("employees_count", [1])
def test_generate_employees(employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count)

    file_path = os.path.join(AppFolders.RESOURCES_PATH, f"employees{employees_count}.csv")
    column_names = ["First Name", "Last Name", "Email"]
    CSVTool.create_file(employees_list, column_names, file_path)


@pytest.mark.parametrize("employees_count", [5])
def test_simulation_campaign(api_request_context_customer_admin, clean_up_employees, api_request_context_aw_admin,
                             employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count, domain="aironworks.com")

    response = CompanyService.create_employees(api_request_context_customer_admin, employees_list, overwrite=True)
    assert response.ok, f"{response.json()}"

    response = CompanyService.get_employee_ids(api_request_context_customer_admin,
                                               EmployeeListIdsModel(employee_role=True, filters=None))
    employee_ids = response.json()
    assert len(employee_ids["items"]) == employees_count, \
        f"Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}"

    response = ScenarioService.post_list_attack_infos(api_request_context_customer_admin,
                                                      ListAttackInfosModelFactory.get_list_attack_infos())
    list_attack_infos = ListAttackInfosResponseModel.from_dict(response.json())
    assert len(list_attack_infos.infos) > 0
    infos = list_attack_infos.infos[0]
    response = LoginService.info(api_request_context_customer_admin)
    campaign_model = CampaignModelFactory.get_campaign(name=infos.strategy_name,
                                                       company_id=response.json()['user']['company_id'],
                                                       employees=employee_ids["items"], attack_info_id=infos.id)
    response = AdminService.campaign(api_request_context_customer_admin, campaign_model)

    campaign_urls = ScenarioService.aw_admin_campaign_urls(api_request_context_aw_admin,
                                                           campaign_id=response.json()['id'])
    file_path = os.path.join(AppFolders.RESOURCES_PATH, "perf_warning_page.csv")
    fieldnames = campaign_urls.attacks[0].get_fieldnames()
    CSVTool.create_file(campaign_urls.attacks, fieldnames, file_path)
