import allure
from playwright.sync_api import Locator, Page, expect

from src.models.auth.user_model import UserModel
from src.page_objects.base_page import BasePage
from src.page_objects.content_library import (
    ContentType,
    new_content_successfully_published_text,
    pdf_file_attached_text,
    sensitive_information_description_text,
)
from src.page_objects.content_library.attach_assessment_page import AddAssessmentPage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.entity.content_library_entity import ContentLibraryEntity


class AddContentPage(BasePage):
    def __init__(self, page: Page, content_type: ContentType):
        super().__init__(page)
        self.content_type = content_type
        self.general_information = GeneralInformationComponent(
            self.page.get_by_label('General information')
        )
        self.additional_information = AdditionalInformationComponent(
            self.page.get_by_label('Additional information')
        )
        self.sensitive_information = SensitiveInformationComponent(
            self.page.get_by_label('Sensitive information')
        )
        self.content_visibility = ContentVisibilityComponent(
            self.page.get_by_label('Content visibility')
        )
        self.quiz = QuizComponent(self.page.get_by_label('Quiz'))
        self.assessment_form = AssessmentFormComponent(
            self.page.get_by_label('Assessment Form')
        )
        self.save_and_publish_button = self.page.get_by_text('Save and Publish')

    @allure.step('AddContentPage: create education content {education_content}')
    def create_content(self, education_content: ContentLibraryEntity, user: UserModel):
        if user.is_admin:
            expect(self.sensitive_information.description).to_contain_text(
                sensitive_information_description_text
            )
            self.sensitive_information.apply_sensitive_information(
                education_content.sensitive_information
            )
            if education_content.sensitive_information:
                expect(self.content_visibility.for_all_button).not_to_be_visible()
        else:
            expect(self.content_visibility.locator).not_to_be_visible()
        self.general_information.fill_data(education_content)
        if education_content.content_type == ContentType.PDF:
            self.upload_pdf_file(education_content)
        elif education_content.content_type == ContentType.ASSESSMENT:
            self.add_assessment(education_content)
        self.save_and_publish_button.click()
        expect(self.alert_message).to_contain_text(
            new_content_successfully_published_text
        )

    @allure.step('AddContentPage: upload pdf file')
    def upload_pdf_file(self, education_content: ContentLibraryEntity):
        with self.page.expect_file_chooser() as fc:
            self.general_information.upload_pdf_button.click()
            fc.value.set_files(education_content.pdf_file_path)
        expect(self.alert_message).to_contain_text(
            pdf_file_attached_text, timeout=20_000
        )

    @allure.step('AddContentPage: add assessment {education_content}')
    def add_assessment(self, education_content: ContentLibraryEntity):
        self.assessment_form.attach_assessment_button.click()
        AddAssessmentPage(self.page).apply_assessment(education_content.assessment)


class GeneralInformationComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.link = self.locator.locator('[name="link"]')
        self.title = self.locator.locator('[name="title"]')
        self.description = self.locator.locator('[name="description"]')
        self.thumbnail_path_button = self.locator.locator('[id="thumbnail_path"]')
        self.upload_pdf_button = self.locator.locator('[id="file_path"]')

    @allure.step('GeneralInformationComponent: fill data')
    def fill_data(self, education_content: ContentLibraryEntity):
        if education_content.title:
            self.title.fill(education_content.title)
        if education_content.url:
            self.link.fill(education_content.url)


class AdditionalInformationComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.topic = self.locator.locator('[id="topic"]')
        self.difficulty = DropDown(
            link_locator=self.locator.locator('[aria-labelledby="difficulty-label"]'),
            option_list_locator=self.locator.locator('[role="option"]'),
        )
        self.industry = DropDown(
            link_locator=self.locator.locator('[id="industry"]'),
            option_list_locator=self.locator.locator('[role="option"]'),
        )

    @allure.step('AdditionalInformationComponent: fill data')
    def fill_data(self, education_content: ContentLibraryEntity):
        if education_content.topic:
            self.topic.fill(education_content.topic)


class SensitiveInformationComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.not_contains_button = self.locator.locator('[aria-label="Not Contains"]')
        self.contains_button = self.locator.locator('[aria-label="Contains"]')
        self.title = self.locator.locator('//div/p').first
        self.description = self.locator.locator('//div/p').last

    @allure.step(
        'SensitiveInformationComponent: apply sensitive information {is_contains_sensitive_information}'
    )
    def apply_sensitive_information(self, is_contains_sensitive_information: bool):
        if is_contains_sensitive_information:
            self.contains_button.click()
        else:
            self.not_contains_button.click()


class ContentVisibilityComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.for_all_button = self.locator.locator('[aria-label="For All"]')
        self.specific_companies_button = self.locator.locator(
            '[aria-label="Specific Companies"]'
        )
        self.hidden_button = self.locator.locator('[aria-label="Hidden"]')

        self.specific_companies = DropDown(
            link_locator=self.locator.locator('[id="companies"]'),
            option_list_locator=self.locator.locator('[role="option"]'),
        )


class QuizComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.attach_quiz_button = self.locator.get_by_role('button')


class AssessmentFormComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.attach_assessment_button = self.locator.get_by_role('button')
