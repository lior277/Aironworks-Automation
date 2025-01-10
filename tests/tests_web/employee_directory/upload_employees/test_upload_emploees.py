import os
import random
import string

import allure
import pytest

from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.page_objects.const import update_succeeded_text
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.utils.csv_tool import CSVTool


class TestUploadEmployees:
    @pytest.fixture(scope='function')
    def generate_employees_file(
        self, request, api_request_context_customer_admin_upload, is_csv_file
    ) -> str:
        def finalizer():
            os.remove(file_path)

        request.addfinalizer(finalizer)
        employees_list = EmployeeModelFactory.get_random_employees(10)
        file_extension = '.csv' if is_csv_file else '.xlsx'
        file_path = os.path.join(
            AppFolders.RESOURCES_PATH,
            f"employees{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}{file_extension}",
        )
        column_names = ['First Name', 'Last Name', 'Email']
        if is_csv_file:
            return CSVTool.create_file(employees_list, column_names, file_path)
        else:
            return CSVTool.create_xlsx_file(employees_list, column_names, file_path)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,override,is_csv_file',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                True,
                True,
                marks=allure.testcase('31539'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                False,
                True,
                marks=allure.testcase('31656'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                True,
                False,
                marks=allure.testcase('31660'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                False,
                False,
                marks=allure.testcase('31661'),
            ),
        ],
    )
    @pytest.mark.single_thread
    def test_upload_employees(
        self,
        employee_directory_page: EmployeeDirectoryPage,
        user: UserModel,
        override: bool,
        generate_employees_file,
        is_csv_file: bool,
    ):
        employee_directory_page.upload_file(generate_employees_file, override)
        employee_directory_page.ensure_alert_message_is_visible(update_succeeded_text)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,with_additional_fields',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                True,
                marks=allure.testcase('31665'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                False,
                marks=allure.testcase('31662'),
            ),
        ],
    )
    def test_upload_employees_with_updated_csv_example_file(
        self,
        employee_directory_page: EmployeeDirectoryPage,
        user: UserModel,
        with_additional_fields: bool,
    ):
        file_path = employee_directory_page.download_csv_file(with_additional_fields)
        employees_list = EmployeeModelFactory.get_random_employees(15)
        CSVTool.update_csv_file(file_path, employees_list)
        employee_directory_page.upload_file(file_path)
        employee_directory_page.ensure_alert_message_is_visible(update_succeeded_text)
