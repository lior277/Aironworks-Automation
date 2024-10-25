import io
from csv import DictWriter
from datetime import datetime, timedelta

import allure
from playwright.sync_api import APIRequestContext, APIResponse, expect

from src.apis.api_factory import api
from src.apis.education import EducationCampaignModel
from src.configs.config_loader import AppConfigs
from src.models.company.employee_model import EmployeeModel
from src.models.general_models import LongRunningOperation
from src.utils.mailtrap import find_email
from src.utils.waiter import wait_for_lro


@allure.step('run education campaign on employee')
def run_education_campaign_on_employee(
    request_context: APIRequestContext, mailtrap, employee
):
    education = api.education(request_context)
    result = education.start_campaign(
        EducationCampaignModel(
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            start_date=datetime.now().timestamp(),
            end_date=(datetime.now() + timedelta(days=1)).timestamp(),
            employee_ids=[employee.employee_id],
            content_id=AppConfigs.EXAMPLE_EDUCATION_CONTENT,
        )
    )
    expect(result).to_be_ok()

    assert 'id' in result.json()
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email)
    )
    return mail


@allure.step('create employees')
def create_employees(
    request_context: APIRequestContext,
    employees: list[EmployeeModel],
    overwrite: bool = False,
) -> APIResponse:
    buffer = io.StringIO()
    writer = DictWriter(buffer, fieldnames=['first_name', 'last_name', 'email'])
    writer.writerow(
        {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
    )
    for employee in employees:
        writer.writerow(
            {
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'email': employee.email,
            }
        )
    buffer.flush()
    buffer.seek(0)
    data = buffer.read().encode('utf-8')
    path = api.upload(request_context).upload_file(
        'employees.csv', 'text/csv', data, 'TEMPORARY'
    )
    return api.company(request_context).create_employees(path, overwrite)


@allure.step('create employees and wait until upload file finished')
def create_employees_wait(
    request_context: APIRequestContext,
    employees: list[EmployeeModel],
    overwrite: bool = False,
) -> APIResponse:
    response = create_employees(request_context, employees, overwrite)
    expect(response).to_be_ok()
    response_body = LongRunningOperation.from_dict(response.json())
    assert (
        response_body.status == 'CREATED'
        or response_body.status == 'IN_PROGRESS'
        or response_body.status == 'DONE'
    )
    operation_id = response_body.id
    company = api.company(request_context)
    result = wait_for_lro(
        lambda: company.create_employees_status(operation_id), timeout=60 * 2
    )
    expect(result).to_be_ok()
    response_body = LongRunningOperation.from_dict(result.json())

    assert (
        response_body.status == 'DONE'
    ), f'Failed to upload file with employee. Response => {response_body}'
    return result


@allure.step('create {employee} employee')
def create_employee(
    request_context: APIRequestContext, employee: EmployeeModel
) -> APIResponse:
    return create_employees_wait(request_context, [employee], False)
