import os

import pandas as pd
import pytest

from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.groups.groups_page import GroupsPage


class TestDownloadExampleCSVFile:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,expected_file',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                'example3.csv',
                marks=pytest.mark.test_id('C3171'),
            )
        ],
    )
    def test_download_example_csv_file(
        self, groups_page: GroupsPage, user: UserModel, expected_file: str
    ):
        df2 = pd.read_csv(os.path.join(AppFolders.RESOURCES_PATH, expected_file))
        file_path = groups_page.download_csv_file()
        df1 = pd.read_csv(file_path)
        assert df1.equals(df2), f'{df1.items=}\n\n{df2.items=}'
