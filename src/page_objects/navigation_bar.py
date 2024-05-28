import allure
from playwright.sync_api import Page
from src.page_objects.scenarios_page import ScenariosPage
from src.page_objects.settings_page import SettingsPage
from src.page_objects.employee_reports_page import EmployeeReportsPage
from src.page_objects.content_library_page import ContentLibraryPage
from src.page_objects.campaigns_page import CampaignsPage


class NavigationBar:
    def __init__(self, page: Page):
        self.page = page
        self.scenarios_button = page.get_by_role("link", name="Scenarios")
        self.settings_button = page.get_by_role("link", name="Settings")
        self.employee_reports_button = page.get_by_role(
            "link", name="PhishDetect AI Reports"
        )
        self.content_library_button = page.get_by_role("link", name="Content Library")
        self.campaigns_button = page.get_by_role("link", name="Campaigns", exact=True)

    @allure.step("NavigationBar: Navigate to scenarios")
    def navigate_scenarios(self):
        self.scenarios_button.click()
        self.page.wait_for_load_state(timeout=5)

        return ScenariosPage(self.page)

    @allure.step("NavigationBar: Navigate to settings")
    def navigate_settings(self):
        self.settings_button.click()
        self.page.wait_for_load_state(timeout=5)

        return SettingsPage(self.page)

    @allure.step("NavigationBar: Navigate to employee reports")
    def navigate_employee_reports(self):
        self.employee_reports_button.click()
        self.page.wait_for_load_state(timeout=5)

        return EmployeeReportsPage(self.page)

    @allure.step("NavigationBar: Navigate to content library")
    def navigate_content_library(self):
        self.content_library_button.click()
        self.page.wait_for_load_state(timeout=5)

        return ContentLibraryPage(self.page)

    @allure.step("NavigationBar: Navigate to campaigns")
    def navigate_campaigns(self):
        self.campaigns_button.click()
        self.page.wait_for_load_state(timeout=5)

        return CampaignsPage(self.page)
