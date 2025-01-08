from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class PhishDetectAISettings(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.title = self.page.locator('[data-testid="heading"]')
        self.general_tab = self.page.get_by_role(role='tab', name='General')
        self.ui_configuration_tab = self.page.get_by_role(
            role='tab', name='Configuration'
        )
