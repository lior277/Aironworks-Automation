import os

import pytest

from src.apis.company import CompanyService
from src.apis.education import EducationService
from src.configs.config_loader import AppFolders
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_assignments import EducationAssignmentsModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import EducationCampaignModelFactory
from src.models.general_models import BasicModel
from src.utils.csv_tool import CSVTool


@pytest.mark.parametrize("employees_count", [1000])
def test_education_campaign(api_request_context_customer_admin, api_request_context_aw_admin, employees_count: int):
    employees_list = EmployeeModelFactory.get_random_employees(employees_count)
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
