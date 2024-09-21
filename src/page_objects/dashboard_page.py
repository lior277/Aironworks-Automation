from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.drop_down_log_out = page.locator('.simplebar-content >div>button')
        self.header = self.page.get_by_role('heading', level=2, name='Dashboard')
