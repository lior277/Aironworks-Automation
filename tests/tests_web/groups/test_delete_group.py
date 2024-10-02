import allure
import pytest
from playwright.sync_api import expect

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.groups.groups_page import GroupsPage


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('31730'))],
)
def test_delete_group(create_group, groups_page: GroupsPage, user: UserModel):
    group_details_page = groups_page.open_group_details(create_group.group.name)
    group_details_page.delete_group()
    groups_page.search_group(create_group.group.name)
    expect(groups_page.page.get_by_text('No results found')).to_be_visible()
