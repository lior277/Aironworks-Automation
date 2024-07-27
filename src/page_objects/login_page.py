import re

import allure
import pytest
from playwright.sync_api import Page

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.page_objects.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_sign_in_email = page.get_by_text('Sign in with Email')
        self.input_email = page.locator('[name="email"]')
        self.input_password = page.locator('[name="password"]')
        self.button_sign_in = page.get_by_role(
            'button', name=re.compile('sign in$', re.IGNORECASE)
        )

    @allure.step('SignInPage: open page')
    def navigate(self, admin=False):
        self.set_default_url(self.adminBaseUrl if admin else self.customerBaseUrl)
        result = self.page.goto(self.default_url)
        result.request.response()

    @allure.step('SignInPage: submit sing in form with {user} credentials')
    def submit_sign_in_form(self, user: UserModel):
        self.fill_sign_in_form(user)
        if not user.is_admin:
            self.page.wait_for_selector(
                selector="//div[text()='Scenarios']"
            ).wait_for_element_state('visible')
        else:
            self.wait_for_loading_state()

    @allure.step('SignInPage: fill sing in form with {user} credentials')
    def fill_sign_in_form(self, user: UserModel):
        if AppConfigs.ENV.startswith('production') and user.is_admin:
            pytest.skip('Admin login is not available in production')
        self.button_sign_in_email.click()
        self.input_email.fill(user.email)
        self.input_password.fill(user.password)
        self.button_sign_in.click()
