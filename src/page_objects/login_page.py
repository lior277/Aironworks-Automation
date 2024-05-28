import allure
import re
import pytest
from playwright.sync_api import Page, expect

from src.models.auth.user_model import UserModel
from src.page_objects.base_page import BasePage
from src.configs.config_loader import AppConfigs


class SignInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_sign_in_email = page.get_by_text("Sign in with Email")
        self.input_email = page.locator('[name="email"]')
        self.input_password = page.locator('[name="password"]')
        self.button_sign_in = page.get_by_role(
            "button", name=re.compile("sign in$", re.IGNORECASE)
        )

    @allure.step("SignInPage: open page")
    def navigate(self, admin=False):
        if admin:
            result = self.page.goto(self.adminBaseUrl)
        else:
            result = self.page.goto(self.baseUrl)
        result.request.response()

    @allure.step("SignInPage: submit sing in form with {user} credentials")
    def submit_sign_in_form(self, user: UserModel):
        if (
            AppConfigs.ENV.startswith("production")
            and not user.is_reseller
            and user.is_admin
        ):
            pytest.skip("Admin login is not available in production")
        self.button_sign_in_email.click()
        self.input_email.fill(user.email)
        self.input_password.fill(user.password)
        self.button_sign_in.click()
        self.page.wait_for_load_state(timeout=5)
