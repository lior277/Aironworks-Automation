import re

import allure
from playwright.sync_api import Locator, Page

from src.models.education.education_content_model import Item
from src.page_objects.base_page import BasePage
from src.page_objects.content_library import ContentType
from src.page_objects.content_library.add_content_page import AddContentPage
from src.page_objects.content_library.content_library_details_page import (
    ContentLibraryDetailsPage,
)
from src.page_objects.data_types.table_element import Table
from src.utils.date_util import timestamp_to_time


class ContentLibraryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.visibility_filter = self.page.get_by_label('Visibility')
        self.name_filter = self.page.get_by_placeholder('Search by Content Name')
        self.cards = self.page.get_by_label('content-card')
        self.table_cards = Table(self.page.get_by_label('content-card'), ContentCard)
        self.add_content_button = self.page.get_by_text('Add Content')
        self.add_content_component = AddContentComponent(
            self.page.locator("//h2[contains(text(),'Add Content')]/..")
        )

    @allure.step('ContentLibraryPage: Set visibility filter')
    def set_visibility_filter(self, name):
        self.visibility_filter.click()
        self.page.get_by_role('option', name=re.compile('.*' + name)).click()

    @allure.step('ContentLibraryPage: Set {name} name filter')
    def set_name_filter(self, name):
        self.name_filter.fill(name)

    @allure.step('ContentLibraryPage: open content library details page')
    def open_content_library_details_page(self, item: Item):
        self.set_name_filter(item.title)
        self.wait_for_progress_bar_disappears()
        assert len(self.table_cards.get_content()) > 0
        card = self.table_cards.get_row_by_column_value(
            'date_created', timestamp_to_time(item.date_created, '%-m/%-d/%Y')
        )
        card.title.click()
        return ContentLibraryDetailsPage(self.page)

    @allure.step('ContentLibraryPage: open add content page')
    def open_add_content_page(self, content_type: ContentType) -> AddContentPage:
        self.add_content_button.click()
        self.add_content_component.add_content(content_type)
        return AddContentPage(self.page, content_type)


class ContentCard:
    def __init__(self, locator: Locator):
        self.title = locator.get_by_role('heading', level=3)
        self.attached = locator.get_by_label('Attached to the Education Campaigns.')
        self.date_created = locator.locator('//*[@id="calendar 1"]/../..')
        self.content_visibility = locator.locator('[data-testid="content-visibility"]')


class AddContentComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.video_button = self.locator.get_by_text('Video', exact=True)
        self.slides_button = self.locator.get_by_text('Slides', exact=True)
        self.pdf_button = self.locator.get_by_text('PDF', exact=True)
        self.assessment_button = self.locator.get_by_text('Assessment', exact=True)

    @allure.step('AddContentComponent: add {content_type} content type')
    def add_content(self, content_type: ContentType):
        match content_type:
            case ContentType.VIDEO:
                self.video_button.click()
            case ContentType.SLIDES:
                self.slides_button.click()
            case ContentType.PDF:
                self.pdf_button.click()
            case ContentType.ASSESSMENT:
                self.assessment_button.click()
        self.locator.wait_for(state='hidden')
