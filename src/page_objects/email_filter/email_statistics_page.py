from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class EmailStatisticsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
