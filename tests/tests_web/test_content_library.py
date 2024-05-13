import pytest
from playwright.sync_api import expect
from src.models.factories.user_model_factory import UserModelFactory


@pytest.mark.parametrize("user", [UserModelFactory.aw_admin()])
@pytest.mark.test_id("C31520")
def test_filter_company_by_visiblity(user, sign_in_page):
    sign_in_page.navigate(admin=user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    content_library_page = sign_in_page.navigation_bar.navigate_content_library()
    content_library_page.set_visibility_filter("Test Company 75000")

    expect(content_library_page.cards).to_have_count(1)
