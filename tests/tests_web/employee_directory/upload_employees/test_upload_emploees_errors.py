import os
import random
import string

import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.page_objects import upload_error_message
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.utils.csv_tool import CSVTool


class TestUploadEmployeesErrors:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,file',
        [
            pytest.param(
                UserModelFactory.customer_admin(),
                'sample.pdf',
                marks=pytest.mark.test_id('C31651'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                'sample.txt',
                marks=pytest.mark.test_id('C31655'),
            ),
        ],
    )
    def test_unsupported_files_extension(
        self, employee_directory_page: EmployeeDirectoryPage, user: UserModel, file: str
    ):
        file_path = os.path.join(AppFolders.RESOURCES_PATH, file)
        employee_directory_page.upload_file(file_path)


class TestUploadEmployeesUnsupportedColumns:
    @pytest.fixture(scope='function')
    def generate_employees_file(self, request, columns: list) -> str:
        def finalizer():
            os.remove(file_path)

        request.addfinalizer(finalizer)
        employees_list = EmployeeModelFactory.get_random_employees(1)

        file_path = os.path.join(
            AppFolders.RESOURCES_PATH,
            f"employees{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.csv",
        )
        column_names = ['First Name', 'Last Name', 'Email']
        data_to_update = {}
        for column in columns:
            column_names.append(column)
            data_to_update = {column: 'unsupported value'}

        return CSVTool.create_file(
            employees_list, column_names, file_path, data_to_update
        )

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,columns',
        [
            pytest.param(
                UserModelFactory.customer_admin(),
                ['unsupported field 1', 'unsupported field 2', 'unsupported field 3'],
                marks=pytest.mark.test_id('C31657'),
            )
        ],
    )
    def test_unsupported_columns(
        self,
        employee_directory_page: EmployeeDirectoryPage,
        user: UserModel,
        generate_employees_file,
        columns: list,
    ):
        employee_directory_page.upload_file(generate_employees_file)
        expect(employee_directory_page.alert_message).to_contain_text(
            upload_error_message(columns)
        )
