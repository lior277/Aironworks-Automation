"""Login page object."""

import allure
from playwright.sync_api import Page, expect

from v2.src.core.config import Config


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        # Prefer stable selectors (data-testid). Fallbacks kept as last resort.
        self.email = page.get_by_label('Email').or_(page.locator('input[type="email"]'))
        self.password = page.get_by_label('Password').or_(
            page.locator('input[type="password"]')
        )
        self.submit = page.get_by_role('button', name='Sign in').or_(
            page.locator('button[type="submit"]')
        )

    @allure.step('Open login page')
    def open(self) -> 'LoginPage':
        self.page.goto(f'{Config.BASE_URL}/login', wait_until='domcontentloaded')
        return self

    @allure.step('Login with email: {email}')
    def login(self, email: str, password: str) -> None:
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

        # Best-effort: ensure navigation or a known post-login element.
        # Replace with a real selector from your app.
        expect(self.page).to_have_url(lambda url: '/dashboard' in url or '/home' in url)

    @allure.step('Login default user')
    def login_default_user(self) -> None:
        self.login(Config.USER_EMAIL, Config.USER_PASSWORD)
