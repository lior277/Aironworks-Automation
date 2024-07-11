import re

import allure
from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class ContentLibraryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.visiblity_filter = self.page.get_by_label("Visibility")
        self.name_filter = self.page.get_by_placeholder("Search by Content Name")
        self.cards = self.page.get_by_label("content-card")

    @allure.step("ContentLibraryPage: Set visibility filter")
    def set_visibility_filter(self, name):
        self.visiblity_filter.click()
        self.page.get_by_role("option", name=re.compile(".*" + name)).click()

    @allure.step("ContentLibraryPage: Set name filter")
    def set_name_filter(self, name):
        self.name_filter.fill(name)
