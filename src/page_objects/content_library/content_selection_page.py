import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table


class ContentSelectionPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.name_filter = self.page.get_by_placeholder('Search by Content Name')
        self.cards = self.page.get_by_label('content-card')
        self.table_cards = Table(
            self.page.get_by_role('button', name='content-card'), ContentCard
        )
        self.next_button = self.page.get_by_role('button', name='Next', exact=True)
        self.cancel_button = self.page.get_by_role('button', name='Cancel')

    @allure.step('ContentLibraryPage: Set {name} name filter')
    def set_name_filter(self, name):
        self.name_filter.fill(name)

    def select_content(self, name: str):
        self.table_cards.get_row_by_column_value('title', name).title.click()

    def complete_selection(self):
        self.next_button.click()


class ContentCard:
    def __init__(self, locator: Locator):
        self.title = locator.get_by_role('heading', level=3)
        self.attached = locator.get_by_label('Attached to the Education Campaigns.')
        self.date_created = locator.locator('//*[@id="calendar 1"]/../..')
        self.content_visibility = locator.locator('[data-testid="content-visibility"]')
        self.checkbox = locator.get_by_role('checkbox')
