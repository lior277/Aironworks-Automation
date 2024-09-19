import allure
from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class CampaignsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.default_url + 'admin/dashboard/attacks/executions/'

    @allure.step('CampaignsPage: wait for tables load')
    def wait_for_tables_load(self):
        self.wait_for_progress_bar_disappears()
        self.wait_for_loading_state()
