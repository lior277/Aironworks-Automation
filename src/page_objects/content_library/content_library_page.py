import re

import allure
from playwright.sync_api import Page, Locator

from src.models.education.education_content_model import Item
from src.page_objects.base_page import BasePage
from src.page_objects.content_library.content_library_details_page import ContentLibraryDetailsPage
from src.page_objects.data_types.table_element import Table
from src.utils.date_util import timestamp_to_time


class ContentLibraryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.visibility_filter = self.page.get_by_label("Visibility")
        self.name_filter = self.page.get_by_placeholder("Search by Content Name")
        self.cards = self.page.get_by_label("content-card")
        self.table_cards = Table(page.get_by_label("content-card"), ContentCard)

    @allure.step("ContentLibraryPage: Set visibility filter")
    def set_visibility_filter(self, name):
        self.visibility_filter.click()
        self.page.get_by_role("option", name=re.compile(".*" + name)).click()

    @allure.step("ContentLibraryPage: Set {name} name filter")
    def set_name_filter(self, name):
        self.name_filter.fill(name)

    @allure.step("ContentLibraryPage: open content library details page")
    def open_content_library_details_page(self, item: Item):
        self.set_name_filter(item.title)
        self.wait_for_progress_bar_disappears()
        assert len(self.table_cards.get_content()) > 0
        card = self.table_cards.get_row_by_column_value("date_created",
                                                        timestamp_to_time(item.date_created, "%-m/%-d/%Y"))
        card.title.click()
        return ContentLibraryDetailsPage(self.page)


class ContentCard:
    def __init__(self, locator: Locator):
        self.title = locator.get_by_role("heading", level=3)
        self.attached = locator.get_by_label("Attached to the Education Campaigns.")
        self.date_created = locator.locator('//*[@id="calendar 1"]/../..')
        self.content_visibility = locator.locator('[data-testid="content-visibility"]')
