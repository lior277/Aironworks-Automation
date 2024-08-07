import os

import pandas as pd
import pytest

from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.employee_directory_page import EmployeeDirectoryPage


class TestDownloadExampleCSVFiles:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,expected_file,with_additional_fields',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                'example1.csv',
                True,
                marks=pytest.mark.test_id('C31659'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                'example2.csv',
                False,
                marks=pytest.mark.test_id('C31658'),
            ),
        ],
    )
    def test_download_example_csv_file(
        self,
        employee_directory_page: EmployeeDirectoryPage,
        user: UserModel,
        expected_file: str,
        with_additional_fields: bool,
    ):
        df2 = pd.read_csv(os.path.join(AppFolders.RESOURCES_PATH, expected_file))
        file_path = employee_directory_page.download_csv_file(with_additional_fields)
        df1 = pd.read_csv(file_path)
        assert df1.equals(df2), f'{df1.items=}\n\n{df2.items=}'
