import os

import allure
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
                marks=allure.testcase('31714'),
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


class TestDownloadAsCSV:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user',
        [
            pytest.param(
                UserModelFactory.customer_admin(), marks=allure.testcase('31770')
            )
        ],
    )
    def test_download_as_csv_file(
        self,
        delete_group,
        get_group_managers_and_employees,
        groups_page: GroupsPage,
        user: UserModel,
    ):
        group_employee = get_group_managers_and_employees[1]
        edit_group_page = groups_page.open_edit_group_page(delete_group.group.name)
        file = edit_group_page.export_as_csv()
        file_content = pd.read_csv(file)
        expected_row = [group_employee.email, group_employee.full_name]
        assert list(file_content.values[0]) == expected_row, (
            f'{list(file_content.values[0])=}\n\n{expected_row=}'
        )
        assert len(file_content) == 1, f'{len(file_content)=}'
