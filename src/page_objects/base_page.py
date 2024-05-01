from playwright.sync_api import Page

from src.configs.config_loader import AppConfigs


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.baseUrl = AppConfigs.BASE_URL
        self.adminBaseUrl = AppConfigs.ADMIN_BASE_URL
