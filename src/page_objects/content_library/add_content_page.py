import allure
from playwright.sync_api import Locator, Page, expect

from src.models.auth.user_model import UserModel
from src.page_objects.base_page import BasePage
from src.page_objects.content_library.attach_quiz_page import AddQuizPage
from src.page_objects.content_library.attach_survey_page import AddSurveyPage
from src.page_objects.content_library.const import (
    ContentType,
    new_content_successfully_published_text,
    pdf_file_attached_text,
    sensitive_information_description_text,
)
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
        self.quiz_form = QuizFormComponent(self.page.get_by_label('Quiz Form'))
        self.survey = SurveyComponent(self.page.get_by_label('Survey'))
        self.survey_form = SurveyFormComponent(self.page.get_by_label('Poll'))
        self.save_and_publish_button = self.page.get_by_text('Save and Publish')
        self.language_dropdown = DropDown(
            link_locator=self.page.locator('[aria-labelledby="language-label"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )

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
        self.language_dropdown.select_item_by_text(education_content.language)
        if education_content.content_type == ContentType.PDF:
            self.upload_pdf_file(education_content)
        elif education_content.content_type == ContentType.QUIZ:
            self.add_quiz(education_content)
        elif education_content.content_type == ContentType.SURVEY:
            self.add_survey(education_content)
        self.save_and_publish_button.click()
        self.ensure_alert_message_is_visible(new_content_successfully_published_text)

    @allure.step('AddContentPage: upload pdf file')
    def upload_pdf_file(self, education_content: ContentLibraryEntity):
        with self.page.expect_file_chooser() as fc:
            self.general_information.upload_pdf_button.click()
            fc.value.set_files(education_content.pdf_file_path)
        self.ensure_alert_message_is_visible(pdf_file_attached_text, timeout=20_000)

    @allure.step('AddContentPage: add quiz {education_content}')
    def add_quiz(self, education_content: ContentLibraryEntity):
        self.quiz_form.attach_quiz_button.click()
        AddQuizPage(self.page).apply_quiz(education_content.quiz)

    @allure.step('AddContentPage: add survey {education_content}')
    def add_survey(self, education_content: ContentLibraryEntity):
        self.survey_form.attach_survey_button.click()
        AddSurveyPage(self.page).apply_survey(education_content.survey)


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
        if education_content.description:
            self.description.fill(education_content.description)
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
        self.description = self.locator.locator('//div[2]/p[2]')

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


class QuizFormComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.attach_quiz_button = self.locator.get_by_role('button')


class SurveyComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.attach_survey_button = self.locator.get_by_role('button')


class SurveyFormComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.attach_survey_button = self.locator.get_by_role('button')
