import allure
from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.add_content_page import (
    AdditionalInformationComponent,
    ContentVisibilityComponent,
    GeneralInformationComponent,
)
from src.page_objects.content_library.const import (
    ContentType,
    attach_quiz_text,
    content_successfully_updated_text,
    education_content_cloned_text,
)
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.entity.content_library_entity import ContentLibraryEntity


class ContentLibraryDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.default_url + 'admin/dashboard/content-library/'
        self.edit_button = self.page.locator(
            selector="[data-testid='EditOutlinedIcon']"
        )
        self.clone_button = self.page.get_by_role('button', name='Clone')

        self.remove_quiz_button = self.page.get_by_text(text='Delete Quiz')
        self.create_education_campaign_button = self.page.get_by_text(
            text='Create Education Campaign'
        )
        self.delete_button = self.page.get_by_text(text='Yes, Delete')
        self.language_dropdown = DropDown(
            link_locator=self.page.locator('[aria-labelledby="language-label"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.general_information = GeneralInformationComponent(
            self.page.get_by_label('General information')
        )
        self.additional_information = AdditionalInformationComponent(
            self.page.get_by_label('Additional information')
        )

        self.content_visibility = ContentVisibilityComponent(
            self.page.get_by_label('Content visibility')
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
        self.ensure_alert_message_is_visible(content_successfully_updated_text)
        expect(self.page.get_by_text(attach_quiz_text)).to_be_visible()
        return self

    @allure.step('ContentLibraryDetailsPage: clone content')
    def clone_content(self):
        expected_title = 'Clone - ' + self.general_information.title.get_attribute(
            'value'
        )
        self.clone_button.click()
        self.ensure_alert_message_is_visible(education_content_cloned_text)
        expect(self.general_information.title).to_have_attribute(
            name='value', value=expected_title
        )

    @allure.step('ContentLibraryDetailsPage: get content library entity')
    def get_content_library_entity(
        self, content_type: ContentType
    ) -> ContentLibraryEntity:
        return ContentLibraryEntity(
            title=self.general_information.title.get_attribute('value'),
            description=self.general_information.description.text_content(),
            language=self.language_dropdown.locator.text_content(),
            topic=self.additional_information.topic.get_attribute('value'),
            difficulty=self.get_difficulty(content_type),
            industry=self.additional_information.industry.locator.get_attribute(
                'value'
            ),
            sensitive_information=False,
            content_type=content_type,
            url=self.general_information.link.get_attribute('value')
            if content_type == ContentType.VIDEO
            else None,
        )

    @allure.step('ContentLibraryDetailsPage: get sensitive information')
    def get_sensitive_information(self) -> bool:
        if self.content_visibility.for_all_button.is_visible():
            return eval(
                self.content_visibility.for_all_button.get_attribute(
                    'aria-pressed'
                ).title()
            )
        else:
            return False

    @allure.step('ContentLibraryDetailsPage: difficulty')
    def get_difficulty(self, content_type: ContentType):
        match content_type:
            case ContentType.QUIZ | ContentType.SURVEY:
                return None
            case _:
                return self.additional_information.difficulty.locator.text_content()

    @allure.step('ContentLibraryDetailsPage: get content id')
    def get_content_id(self) -> str:
        return self.page.url.split('/')[-1]
