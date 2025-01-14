import logging
import os
import time

import pytest

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees, create_employees_wait
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
from src.models.scenario.list_attack_infos_response_model import (
    ListAttackInfosResponseModel,
)
from src.models.survey.get_survey import GetSurveyModel
from src.models.survey.surveys_model import Survey
from src.utils.json_tool import JSONTool


@pytest.mark.parametrize('employees_count', [2])
@pytest.mark.prepare_data
def test_education_campaign(
    api_request_context_customer_admin,
    clean_up_employees,
    api_request_context_aw_admin,
    employees_count: int,
):
    employees_list = EmployeeModelFactory.get_random_employees(
        employees_count, domain='aironworks.com'
    )
    company = api.company(api_request_context_customer_admin)
    education = api.education(api_request_context_customer_admin)
    response = create_employees(
        api_request_context_customer_admin, employees_list, overwrite=True
    )
    assert response.ok, f'{response.json()}'
    time.sleep(5)
    response = company.get_employee_ids(
        EmployeeListIdsModel(employee_role=True, filters=None)
    )
    employee_ids = response.json()
    assert len(employee_ids['items']) == employees_count, (
        f'Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}'
    )
    response = education.get_content_pagination()
    assert response.ok, f'Failed to fetch education content => {response.json()}'
    education_content = EducationContentModel.from_dict(response.json())
    education_campaign = (
        EducationCampaignModelFactory.get_education_campaign_from_education_content(
            education_content.items[0].id, employee_ids['items']
        )
    )
    response = education.start_campaign(education_campaign)
    response = api.education(
        api_request_context_aw_admin
    ).aw_admin_education_assignments(campaign_id=response.json()['id'])
    logging.info(f'response: {response.json()}')
    education_assignments = EducationAssignmentsModel.from_dict(response.json())
    file_path = os.path.join(
        AppFolders.TESTS_PATH, 'tests_perf_k6/perf_education_campaign.json'
    )
    # CSVTool.create_file(education_assignments.assignments, fieldnames, file_path)
    JSONTool.create_file(education_assignments.assignments, file_path)


# @pytest.mark.parametrize('employees_count', [1])
# def test_generate_employees(employees_count: int):
#     employees_list = EmployeeModelFactory.get_random_employees(
#         employees_count,
#         mailtrap_inbox=MailTrapModelFactory.get_perf_mail_trap_inbox().email,
#     )

#     file_path = os.path.join(
#         AppFolders.RESOURCES_PATH, f'employees{employees_count}.json'
#     )
#     JSONTool.create_file(employees_list, file_path)
# CSVTool.create_file(employees_list, column_names, file_path)


@pytest.mark.parametrize('employees_count', [3000])
@pytest.mark.timeout(60 * 60)
@pytest.mark.prepare_data
def test_simulation_campaign(
    api_request_context_customer_admin,
    set_up_perf_survey: Survey,
    api_request_context_aw_admin,
    employees_count: int,
):
    employees_list = EmployeeModelFactory.get_random_employees(
        employees_count, domain='aironworks.com'
    )
    company = api.company(api_request_context_customer_admin)
    scenario_service = api.scenario(api_request_context_customer_admin)
    login_service = api.login(api_request_context_customer_admin)
    survey_service = api.survey(api_request_context_customer_admin)
    response = create_employees_wait(
        api_request_context_customer_admin, employees_list, overwrite=False
    )
    assert response.ok, f'{response.json()}'

    response = company.get_employee_ids(
        EmployeeListIdsModel(employee_role=True, filters=None)
    )
    employee_ids = response.json()
    # assert (
    #     len(employee_ids['items']) == employees_count
    # ), f"Expected employees => {employees_count}\nActual employees => {len(employee_ids["items"])}"

    response = scenario_service.post_list_attack_infos(
        ListAttackInfosModelFactory.get_list_attack_infos()
    )
    logging.info(f'response: {response.json()}')
    list_attack_infos = ListAttackInfosResponseModel.from_dict(response.json())
    assert len(list_attack_infos.infos) > 0
    infos = list_attack_infos.infos[0]
    response = login_service.info()
    campaign_model = CampaignModelFactory.get_campaign(
        campaign_name=infos.strategy_name,
        company_id=response.json()['user']['company_id'],
        employees=employee_ids['items'],
        attack_info_id=infos.id,
        send_attacks=False,
    )
    admin_service = api.admin(api_request_context_customer_admin)
    response = admin_service.start_campaign(campaign_model)

    while True:
        time.sleep(10)
        campaign_urls = api.scenario(
            api_request_context_aw_admin
        ).aw_admin_campaign_urls(campaign_id=response.json()['id'])
        o = campaign_urls.attacks[0].attack_url
        if o is not None:
            break

    file_path = os.path.join(
        AppFolders.TESTS_PATH, 'tests_perf_k6/perf_warning_page.json'
    )
    fieldnames = campaign_urls.attacks[0].get_fieldnames()
    response = survey_service.get_survey(set_up_perf_survey.id)
    assert response.ok, f'{response.json()=}'
    survey = GetSurveyModel.from_dict(response.json())
    fieldnames.extend(['qid', 'option_id', 'survey_id'])
    data_to_update = {
        'qid': f'{survey.model.questions[0].id}',
        'option_id': f'{survey.model.questions[0].options[0].id}',
        'survey_id': f'{survey.model.id}',
    }
    JSONTool.create_file(campaign_urls.attacks, file_path, data_to_update)
    # CSVTool.create_file(campaign_urls.attacks, fieldnames, file_path, data_to_update)
