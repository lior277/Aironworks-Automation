import os
import random
import string

import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppFolders
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.group.group_model_factory import GroupModelFactory
from src.models.group.group_list import GroupListModel
from src.page_objects import update_succeeded_text
from src.page_objects.groups.groups_page import GroupsPage
from src.utils.csv_tool import CSVTool


class TestUploadGroups:
    @pytest.fixture(scope='function')
    def generate_groups_file(
        self, request, is_csv_file, api_request_context_customer_admin
    ) -> str:
        def finalizer():
            os.remove(file_path)
            group_service = api.group(api_request_context_customer_admin)
            response = group_service.get_group_list()
            expect(response).to_be_ok()
            group_list = GroupListModel.from_dict(response.json())
            group_to_delete = next(
                (gr for gr in group_list.groups if gr.name == group.name), None
            )
            if group_to_delete:
                group_service.delete_group(group_to_delete.id)

        request.addfinalizer(finalizer)
        group = GroupModelFactory.get_random_group()
        file_extension = '.csv' if is_csv_file else '.xlsx'
        file_path = os.path.join(
            AppFolders.RESOURCES_PATH,
            f"group{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}{file_extension}",
        )
        column_names = [
            'Group Name',
            'Group Admin Email',
            'Group Admin First Name',
            'Group Admin Last Name',
        ]
        if is_csv_file:
            return CSVTool.create_file(group, column_names, file_path)
        else:
            return CSVTool.create_xlsx_file(group, column_names, file_path)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,is_csv_file',
        [
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                True,
                marks=allure.testcase('31711'),
            ),
            pytest.param(
                UserModelFactory.customer_admin_upload(),
                False,
                marks=allure.testcase('31712'),
            ),
        ],
    )
    def test_upload_groups(
        self,
        generate_groups_file,
        groups_page: GroupsPage,
        user: UserModel,
        is_csv_file: bool,
    ):
        groups_page.upload_file(generate_groups_file)
        expect(groups_page.alert_message).to_contain_text(update_succeeded_text)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,file',
        [
            pytest.param(
                UserModelFactory.customer_admin(),
                'sample.txt',
                marks=allure.testcase('31713'),
            )
        ],
    )
    def test_upload_group_unsupported_files_extension(
        self, groups_page: GroupsPage, user: UserModel, file: str
    ):
        file_path = os.path.join(AppFolders.RESOURCES_PATH, file)
        groups_page.upload_file(file_path)
