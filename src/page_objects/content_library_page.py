import allure
import re
from playwright.sync_api import Page
from src.page_objects.base_page import BasePage


class ContentLibraryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.visiblity_filter = self.page.get_by_label("Visibility")
        self.cards = self.page.get_by_label("content-card")

    @allure.step("ContentLibraryPage: Set visibility filter")
    def set_visibility_filter(self, name):
        self.visiblity_filter.click()
        self.page.get_by_role("option", name=re.compile(".*" + name)).click()
