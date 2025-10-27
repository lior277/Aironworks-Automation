import allure
from playwright.sync_api import Page

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.const import quiz_attached_text
from src.page_objects.entity.content_library_entity import QuizEntity


class AttachQuizPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.question_input = page.get_by_role('textbox', name='Untitled Question')
        self.answer_one_input = page.get_by_role('textbox', name='Answer 1')
        self.answer_two_input = page.get_by_role('textbox', name='Answer 2')
        self.add_new_answer_button = page.get_by_text('Add new Answer')
        self.add_a_question_button = page.get_by_text('Add a Question')
        self.apply_button = page.get_by_text('Apply')
        self.cancel_button = page.get_by_text('Cancel')

    @allure.step('AddQuizPage: apply quiz {quiz}')
    def apply_quiz(self, quiz: QuizEntity):
        if len(quiz.questions) > 1:
            raise ValueError('Fix this method')
        else:
            self.question_input.fill(quiz.questions[0].question)
            self.answer_one_input.fill(quiz.questions[0].answers[0].answer)
            self.answer_two_input.fill(quiz.questions[0].answers[1].answer)
            self.apply_button.click()
            self.ensure_alert_message_is_visible(quiz_attached_text)
            self.ensure_alert_message_is_not_visible(quiz_attached_text)
