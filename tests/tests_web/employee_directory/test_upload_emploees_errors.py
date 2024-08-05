import os

import pytest

from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.employee_directory_page import EmployeeDirectoryPage


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
