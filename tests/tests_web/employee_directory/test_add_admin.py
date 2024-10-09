import allure
import pytest

from src.configs.config_loader import AppConfigs
from src.models.company.employee_model import EmployeeModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.page_objects.employee_directory.add_admin_page import AddAdminPage
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.utils.mailtrap import find_email


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, create_new',
    [
        pytest.param(
            UserModelFactory.customer_admin(), False, marks=allure.testcase('C31787')
        )
    ],
)
def test_add_admin_existing_employee(
    employee_directory_page: EmployeeDirectoryPage,
    add_admin_page: AddAdminPage,
    create_new: bool,
    employee,
    mailtrap,
):
    add_admin_page.add_admin(employee, create_new)


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, employee, create_new',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            EmployeeModelFactory.get_random_employee_with_accessible_email(),
            True,
            marks=allure.testcase('C31786'),
        )
    ],
)
def test_add_admin_new_employee(
    employee_directory_page: EmployeeDirectoryPage,
    add_admin_page: AddAdminPage,
    employee: EmployeeModel,
    create_new: bool,
    mailtrap,
):
    add_admin_page.add_admin(employee, create_new)
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email)
    )
    assert mail is not None, f'Failed to find email for {employee.email}'
