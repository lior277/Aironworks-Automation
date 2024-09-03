import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.groups.groups_page import GroupsPage
from src.utils.randomizer import generate_string


class TestCreateGroup:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user',
        [
            pytest.param(
                UserModelFactory.customer_admin(), marks=pytest.mark.test_id('C29343')
            )
        ],
    )
    def test_create_group_with_name_only(
        self, groups_page: GroupsPage, user: UserModel
    ):
        groups_page.create_group(generate_string())

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user',
        [
            pytest.param(
                UserModelFactory.customer_admin(), marks=pytest.mark.test_id('C29345')
            )
        ],
    )
    def test_create_group_all_fields(
        self, groups_page: GroupsPage, user: UserModel, get_group_managers_and_employees
    ):
        groups_page.create_group(
            generate_string(),
            [get_group_managers_and_employees[0].email],
            [get_group_managers_and_employees[1].email],
        )
