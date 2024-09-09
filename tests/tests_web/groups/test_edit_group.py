import pytest
from playwright.sync_api import expect

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.groups.groups_page import GroupsPage
from src.utils.randomizer import generate_string


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin(), marks=pytest.mark.test_id('C31731')
        )
    ],
)
def test_edit_group(create_group, groups_page: GroupsPage, user: UserModel):
    new_group_name = generate_string()
    edit_group_page = groups_page.open_edit_group_page(create_group.group.name)
    group_detail_page = edit_group_page.edit_group(new_group_name, True, True)
    group_detail_page.back_button.click()
    groups_page.search_group(create_group.group.name)
    expect(groups_page.page.get_by_text('No results found')).to_be_visible()
    groups_page.search_group(new_group_name)
    expect(groups_page.groups_table._Table__locator).to_have_count(1)
