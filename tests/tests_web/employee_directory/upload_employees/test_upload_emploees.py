import os
import random
import string

import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.company.employee_delete_model import EmployeeDeleteModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.company.employee_model_factory import EmployeeModelFactory
from src.page_objects import update_succeeded_text
from src.page_objects.employee_directory_page import EmployeeDirectoryPage
from src.utils.csv_tool import CSVTool


class TestUploadEmployees:
    @pytest.fixture(scope='function')
    def generate_employees_file(
        self, request, api_request_context_customer_admin_upload
    ) -> str:
        def finalizer():
            company_service = api.company(api_request_context_customer_admin_upload)
            response = company_service.get_employee_ids(
                EmployeeListIdsModel(
                    employee_role=False, admin_role=False, filters=None
                )
            )
            expect(response).to_be_ok()
            if response.json()['items']:
                expect(
                    company_service.delete_employees(
                        employees=EmployeeDeleteModel(ids=response.json()['items'])
                    )
                ).to_be_ok()
            response = company_service.get_employee_ids(
                EmployeeListIdsModel(employee_role=True, admin_role=False, filters=None)
            )
            expect(response).to_be_ok()
            if response.json()['items']:
                expect(
                    company_service.delete_employees(
                        employees=EmployeeDeleteModel(ids=response.json()['items'])
                    )
                ).to_be_ok()
            os.remove(file_path)

        request.addfinalizer(finalizer)
        employees_list = EmployeeModelFactory.get_random_employees(10)

        file_path = os.path.join(
            AppFolders.RESOURCES_PATH,
            f"employees{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}.csv",
        )
        column_names = ['First Name', 'Last Name', 'Email']
        return CSVTool.create_file(employees_list, column_names, file_path)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,override',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                True,
                marks=pytest.mark.test_id('C31539'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                False,
                marks=pytest.mark.test_id('C31656'),
            ),
        ],
    )
    def test_upload_employees(
        self,
        employee_directory_page: EmployeeDirectoryPage,
        user: UserModel,
        override: bool,
        generate_employees_file,
    ):
        employee_directory_page.upload_file(generate_employees_file, override)
        expect(employee_directory_page.alert_message).to_contain_text(
            update_succeeded_text
        )
