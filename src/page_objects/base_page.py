from playwright.sync_api import Page

from src.configs.config_loader import AppConfigs


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.baseUrl = AppConfigs.BASE_URL
        self.adminBaseUrl = AppConfigs.ADMIN_BASE_URL
        self.empty_state = self.page.get_by_test_id("empty-state")

        import src.page_objects.navigation_bar

        self.navigation_bar = src.page_objects.navigation_bar.NavigationBar(page)
