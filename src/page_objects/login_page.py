import allure
from playwright.sync_api import Page

from src.models.user_model import UserModel
from src.page_objects.base_page import BasePage


class SignInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_sign_in_email = page.get_by_text('Sign in with Email')
        self.input_email = page.locator('[name="email"]')
        self.input_password = page.locator('[name="password"]')
        self.button_sign_in = page.locator('[id="mui-3"]')

    @allure.step("SignInPage: open page")
    def navigate(self):
        result = self.page.goto(self.baseUrl)
        result.request.response()

    @allure.step("SignInPage: submit sing in form with {user} credentials")
    def submit_sing_in_form(self, user: UserModel):
        self.button_sign_in_email.click()
        self.input_email.fill(user.email)
        self.input_password.fill(user.password)
        self.button_sign_in.click()
        self.page.wait_for_load_state(timeout=5)
