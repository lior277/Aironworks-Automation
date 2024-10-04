import allure
from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.content_library import (
    attach_quiz_text,
    content_successfully_updated_text,
)
from src.page_objects.data_types.drop_down_element import DropDown


class ContentLibraryDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.default_url + 'admin/dashboard/content-library/'
        self.edit_button = self.page.locator(
            selector="[data-testid='EditOutlinedIcon']"
        )
        self.remove_quiz_button = self.page.get_by_text(text='Delete Quiz')
        self.create_education_campaign_button = self.page.get_by_text(
            text='Create Education Campaign'
        )
        self.delete_button = self.page.get_by_text(text='Yes, Delete')
        self.language_dropdown = DropDown(
            link_locator=self.page.locator('[aria-labelledby="language-label"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )

    @allure.step(
        'ContentLibraryDetailsPage: open details page for {content_library_id} content library'
    )
    def open(self, content_library_id: str):
        self.page.goto(self.url + content_library_id)
        self.create_education_campaign_button.wait_for()
        return self

    @allure.step('ContentLibraryDetailsPage: remove quiz')
    def remove_quiz(self):
        self.edit_button.click()
        self.remove_quiz_button.click()
        self.delete_button.click()
        if not self.language_dropdown.locator.text_content() == '':
            self.language_dropdown.select_item_by_text('English')
        self.save_button.click()
        expect(self.alert_message.first).to_contain_text(
            content_successfully_updated_text
        )
        expect(self.page.get_by_text(attach_quiz_text)).to_be_visible()
        return self
