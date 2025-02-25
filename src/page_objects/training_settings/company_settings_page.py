from playwright.sync_api import Locator, Page

from src.page_objects.training_settings.training_settings_page import (
    TrainingSettingsPage,
)


class CompanySettingsPage(TrainingSettingsPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.login_security_section = LoginSecuritySection(
            self.page.get_by_role('region', name='Login Security')
        )

    def select_guest_portal_login_method(self, method: str):
        self.login_security_section.select_login_method(method)


class LoginSecuritySection:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.email_option = self.locator.get_by_role('button', name='Email')
        self.google_sso_option = self.locator.get_by_role('button', name='SSO (Google)')
        self.microsoft_sso_option = self.locator.get_by_role(
            'button', name='SSO (Microsoft)'
        )

    def select_login_method(self, method: str):
        if method == 'email':
            self.email_option.click()
        elif method == 'google':
            self.google_sso_option.click()
        elif method == 'microsoft':
            self.microsoft_sso_option.click()
        else:
            raise ValueError(f'Invalid login method: {method}')
