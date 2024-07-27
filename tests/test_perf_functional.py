import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.apis.steps.common_steps import create_employees
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.company.employee_update_model import EmployeeUpdateModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import (
    EducationCampaignModelFactory,
)
from src.models.general_models import LongRunningOperation
from src.models.mait_trap_model import MailTrapModelFactory
from src.utils.list import divide_list_into_chunks
from src.utils.log import Log
from src.utils.waiter import wait_for_lro

PERF_TIMEOUT = 60 * 120


# max employees_count = 1000
@pytest.mark.parametrize('employees_count', [1])
@pytest.mark.delivered_emails
@pytest.mark.timeout(60 * 100)
def test_education_campaign_emails_delivered(
    api_request_context_customer_admin, mailtrap, employees_count: int
):
    """

    :param api_request_context_customer_admin:
    :param mailtrap:
    :param employees_count: the total number of employees per each inbox,
     currently we have 50 inboxes for performance testing
    """
    employees_list = []
    mail_trap_inboxes = MailTrapModelFactory.get_perf_mail_trap_inboxes()

    # clear all inboxes before test
    Log.info('Clearing all inboxes before test')
    mailtrap.clean_inboxes(mail_trap_inboxes)

    # remove all employees
    Log.info('getting all employees before test')
    company = api.company(api_request_context_customer_admin)
    response = company.get_employee_ids(
        EmployeeListIdsModel(employee_role=True, admin_role=False, filters=None)
    )
    if response.json()['items']:
        Log.info('Updating all employees before test')
        company.update_employees(
            employees=EmployeeUpdateModel(
                employee_role=False, ids=list(response.json()['items'])
            )
        )
    Log.info('getting all employees before test')
    response = company.get_employee_ids(
        EmployeeListIdsModel(employee_role=False, admin_role=False, filters=None)
    )

    if response.json()['items']:
        Log.info('Dividing list into chunks')
        divided_list = divide_list_into_chunks(response.json()['items'], 2000)
        for chunk in divided_list:
            company.delete_employees(employees=EmployeeDeleteModel(ids=chunk))
    # create {employees_count} employees for each inbox
    Log.info('Creating employees for each inbox')
    for mail_trap_inbox in mail_trap_inboxes:
        employees = EmployeeModelFactory.get_random_employees(
            employees_count, mailtrap_inbox=mail_trap_inbox.email
        )
        Log.info(f'Creating employees for inbox {mail_trap_inbox.id}')
        response = create_employees(api_request_context_customer_admin, employees)
        expect(response).to_be_ok()
        response_body = LongRunningOperation.from_dict(response.json())
        assert response_body.status == 'CREATED'
        operation_id = response_body.id
        result = wait_for_lro(
            lambda: company.create_employees_status(operation_id), timeout=60 * 5
        )
        expect(result).to_be_ok()
        response_body = LongRunningOperation.from_dict(result.json())

        assert (
            response_body.status == 'DONE'
        ), f'Failed to upload file with employee. Response => {response_body}'
        employees_list.extend(employees)

    Log.info('Getting employee ids')
    response = company.get_employee_ids(
        EmployeeListIdsModel(employee_role=True, filters=None)
    )
    employee_ids = response.json()
    assert (
        len(employee_ids['items']) >= len(employees_list)
    ), f"Expected employees => {len(employees_list)}\nActual employees => {len(employee_ids["items"])}"
    education_campaign = EducationCampaignModelFactory.get_education_campaign(
        employee_ids['items']
    )

    # start education campaign
    Log.info('Starting education campaign')
    response = api.education(api_request_context_customer_admin).start_campaign(
        education_campaign
    )
    expect(response).to_be_ok()
    employees_email_list = set(employee.email for employee in employees_list)

    # Wait for all emails
    Log.info('Waiting for all emails')
    emails_left = mailtrap.wait_for_all_mail_in_diff_inboxes(
        employees_email_list,
        list_mail_traps=mail_trap_inboxes,
        emails_per_inbox=employees_count,
        remove_messages=False,
        timeout=PERF_TIMEOUT,
    )

    assert not emails_left, f'{len(emails_left)=} {emails_left=}'
