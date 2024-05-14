import pytest
import re
from playwright.sync_api import expect
from src.models.factories.user_model_factory import UserModelFactory


@pytest.mark.parametrize("user", [UserModelFactory.aw_admin()])
@pytest.mark.test_id("C31520")
@pytest.mark.smoke
def test_filter_company_by_visiblity(user, sign_in_page):
    sign_in_page.navigate(admin=user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    content_library_page = sign_in_page.navigation_bar.navigate_content_library()
    content_library_page.set_visibility_filter("Test Company 75000")

    expect(content_library_page.cards).to_have_count(1)


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31518"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31519"),
        ),
    ],
)
@pytest.mark.smoke
def test_filter_company_by_name(user, sign_in_page):
    sign_in_page.navigate(admin=user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    content_library_page = sign_in_page.navigation_bar.navigate_content_library()
    content_library_page.set_name_filter("Authentication 101")

    expect(content_library_page.cards).to_have_count(1)
    expect(content_library_page.cards.first).to_contain_text("Authentication 101")


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31516"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31517"),
        ),
    ],
)
@pytest.mark.smoke
def test_full_state_and_empty_state(user, sign_in_page):
    sign_in_page.navigate(admin=user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    content_library_page = sign_in_page.navigation_bar.navigate_content_library()
    content_library_page.set_name_filter("qwepqwjoeinqwourbqiouwboasnodnqwoienoquwbeq")

    expect(content_library_page.cards).to_have_count(0)
    expect(content_library_page.empty_state).to_be_visible()
    expect(content_library_page.page.get_by_text(re.compile("Oops!.*"))).to_be_visible()
