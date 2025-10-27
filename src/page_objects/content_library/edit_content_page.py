import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.attach_quiz_page import AttachQuizPage
from src.page_objects.content_library.attach_survey_page import AddSurveyPage
from src.page_objects.content_library.const import (
    ContentType,
    content_successfully_updated_text,
)
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.entity.content_library_entity import ContentLibraryEntity


class EditContentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.general_information = GeneralInformationComponent(
            self.page.get_by_label('General information')
        )
        self.additional_information = AdditionalInformationComponent(
            self.page.get_by_label('Additional information')
        )
        self.quiz = QuizComponent(self.page.get_by_label('Quiz'))
        self.survey = SurveyComponent(self.page.get_by_label('Poll'))
        self.save_button = self.page.get_by_role('button', name='Save')

    @allure.step('EditContentPage: edit content {education_content}')
    def edit_content(self, education_content: ContentLibraryEntity):
        self.general_information.update_description_data(education_content)
        if education_content.content_type == ContentType.QUIZ:
            self.edit_quiz(education_content)
        elif education_content.content_type == ContentType.SURVEY:
            self.edit_survey(education_content)
        self.save_button.click()
        self.ensure_alert_message_is_visible(content_successfully_updated_text)

    @allure.step('EditContentPage: edit quiz {education_content}')
    def edit_quiz(self, education_content: ContentLibraryEntity):
        self.quiz.edit_quiz_button.click()
        AttachQuizPage(self.page).apply_quiz(education_content.quiz)

    @allure.step('EditContentPage: edit survey {education_content}')
    def edit_survey(self, education_content: ContentLibraryEntity):
        self.survey.edit_survey_button.click()
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
    def update_description_data(self, education_content: ContentLibraryEntity):
        if education_content.description:
            self.description.fill(education_content.description)


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


class QuizComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.edit_quiz_button = self.locator.get_by_role('button', name='Edit Quiz')
        self.delete_quiz_button = self.locator.get_by_role('button', name='Delete Quiz')


class SurveyComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.edit_survey_button = self.locator.get_by_role('button', name='Edit Survey')
        self.delete_survey_button = self.locator.get_by_role(
            'button', name='Delete Survey'
        )
