"""Login page object."""

from playwright.sync_api import Page

from v2.src.core.config import Config
from v2.src.pages.ui_pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, api_context=None):
        super().__init__(page, api_context)

        # TODO: update selectors to match the real login form if needed
        self.email = page.get_by_label('Email').or_(page.locator('input[type="email"]'))
        self.password = page.get_by_label('Password').or_(
            page.locator('input[type="password"]')
        )
        self.submit = page.get_by_role('button', name='Sign in').or_(
            page.locator('button[type="submit"]')
        )

    def open(self) -> 'LoginPage':
        self.page.goto(f'{Config.BASE_URL}/login')
        return self

    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def login_default_user(self) -> None:
        self.login(Config.USER_EMAIL, Config.USER_PASSWORD)
