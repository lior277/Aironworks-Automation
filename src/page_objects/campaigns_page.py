from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class CampaignsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
