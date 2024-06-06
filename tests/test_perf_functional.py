import pytest

from src.apis.company import CompanyService
from src.apis.education import EducationService
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.company.employee_update_model import EmployeeUpdateModel
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import EducationCampaignModelFactory
from src.models.general_models import BasicModel
from src.models.mait_trap_model import MailTrapModelFactory
from src.utils.list import divide_list_into_chunks


@pytest.mark.parametrize("employees_count", [1])
@pytest.mark.delivered_emails
def test_education_campaign_emails_delivered(api_request_context_customer_admin, mailtrap, employees_count: int):
    """

    :param api_request_context_customer_admin:
    :param mailtrap:
    :param employees_count: the total number of employees per each inbox,
     currently we have 50 inboxes for performance testing
    """
    employees_list = []
    mail_trap_inboxes = MailTrapModelFactory.get_perf_mail_trap_inboxes()

    # clear all inboxes before test
    mailtrap.clean_inboxes(mail_trap_inboxes)

    # remove all employees
    response = CompanyService.get_employee_ids(api_request_context_customer_admin,
                                               EmployeeListIdsModel(employee_role=True, admin_role=False, filters=None))
    if response.json()['items']:
        CompanyService.update_employees(api_request_context_customer_admin,
                                        employees=EmployeeUpdateModel(employee_role=False,
                                                                      ids=list(response.json()['items'])))
    response = CompanyService.get_employee_ids(api_request_context_customer_admin,
                                               EmployeeListIdsModel(employee_role=False, admin_role=False,
                                                                    filters=None))
    if response.json()["items"]:
        divided_list = divide_list_into_chunks(response.json()["items"], 2000)
        for chunk in divided_list:
            CompanyService.delete_employees(api_request_context_customer_admin,
                                            employees=EmployeeDeleteModel(ids=chunk))
    # create {employees_count} employees for each inbox
    for mail_trap_inbox in mail_trap_inboxes:
        employees = EmployeeModelFactory.get_random_employees(employees_count, mailtrap_inbox=mail_trap_inbox.email)
        response = CompanyService.create_employees(api_request_context_customer_admin, employees, overwrite=False)
        response_body = BasicModel.from_dict(response.json())
        assert response_body.data.success and response.ok, \
            f"Failed to upload file with employee. Response => {response_body}"
        employees_list.extend(employees)

    response = CompanyService.get_employee_ids(api_request_context_customer_admin,
                                               EmployeeListIdsModel(employee_role=True, filters=None))
    employee_ids = response.json()
    assert len(employee_ids["items"]) >= len(employees_list), \
        f"Expected employees => {len(employees_list)}\nActual employees => {len(employee_ids["items"])}"
    education_campaign = EducationCampaignModelFactory.get_education_campaign(employee_ids["items"])

    # start education campaign
    response = EducationService.start_campaign(api_request_context_customer_admin, education_campaign)
    assert response.ok
    employees_email_list = [employee.email for employee in employees_list]

    # Wait for all emails
    emails_left = mailtrap.wait_for_all_mail_in_diff_inboxes(employees_email_list, list_mail_traps=mail_trap_inboxes,
                                                             remove_messages=True)

    assert not emails_left, f"{len(emails_left)=} {emails_left=}"
