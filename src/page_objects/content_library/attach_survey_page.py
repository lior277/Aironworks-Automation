import allure
from playwright.sync_api import Page

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.const import survey_attached_text
from src.page_objects.entity.content_library_entity import SurveyEntity


class AddSurveyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.question_input = page.get_by_role('textbox', name='Untitled Question')
        self.answer_one_input = page.get_by_role('textbox', name='Answer 1')
        self.answer_two_input = page.get_by_role('textbox', name='Answer 2')
        self.add_new_answer_button = page.get_by_text('Add new Answer')
        self.add_a_question_button = page.get_by_text('Add A Question')
        self.apply_button = page.get_by_text('Apply')
        self.cancel_button = page.get_by_text('Cancel')

    @allure.step('AddSureveyPage: apply survey {survey}')
    def apply_survey(self, survey: SurveyEntity):
        if len(survey.questions) > 1:
            raise ValueError('Fix this method')
        else:
            self.question_input.fill(survey.questions[0].question)
            self.answer_one_input.fill(survey.questions[0].answers[0])
            self.answer_two_input.fill(survey.questions[0].answers[1])
            self.apply_button.click()
            self.ensure_alert_message_is_visible(survey_attached_text)
            self.ensure_alert_message_is_not_visible()
