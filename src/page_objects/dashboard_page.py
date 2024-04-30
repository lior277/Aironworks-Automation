import allure
from playwright.sync_api import Page

from src.page_objects.base_page import BasePage
from src.page_objects.scenarios_page import ScenariosPage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.drop_down_log_out = page.locator(".simplebar-content >div>button")
        self.scenarios_button = page.get_by_role("link", name="Scenarios")

    @allure.step("DashboardPage: Navigate to scenarios")
    def navigate_scenarios(self):
        self.scenarios_button.click()
        self.page.wait_for_load_state(timeout=5)

        return ScenariosPage(self.page)
