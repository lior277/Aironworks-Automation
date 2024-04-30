import pytest
from playwright.sync_api import expect

from src.models.factories.user_model_factory import UserModelFactory
from src.page_objects.dashboard_page import DashboardPage
from src.page_objects.locators.base_page_locators import BasePageLocators
from src.page_objects.login_page import SignInPage


@pytest.mark.parametrize(
    "user,error_message",
    [
        pytest.param(
            UserModelFactory.user(),
            "Invalid Email address or password",
            id="login invalid user",
            marks=pytest.mark.test_id("C29654"),
        )
    ],
)
@pytest.mark.web
def test_login_error_message(sign_in_page: SignInPage, user, error_message):
    sign_in_page.navigate()
    sign_in_page.submit_sign_in_form(user)
    expect(sign_in_page.page.locator(BasePageLocators.MUI_ALERT_MESSAGE)).to_have_text(
        error_message
    )


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.my_user(),
            id="login success",
            marks=pytest.mark.test_id("C17077"),
        )
    ],
)
def test_login_existing_user(
    sign_in_page: SignInPage, dashboard_page: DashboardPage, user
):
    sign_in_page.navigate()
    sign_in_page.submit_sign_in_form(user)
    expect(dashboard_page.drop_down_log_out).to_contain_text(f"Admin of {user.company}")
