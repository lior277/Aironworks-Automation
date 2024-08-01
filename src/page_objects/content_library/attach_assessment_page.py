import allure
from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.content_library import assessment_attached_text
from src.page_objects.entity.content_library_entity import AssessmentEntity


class AddAssessmentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.question_input = page.get_by_role('textbox', name='Untitled Question')
        self.answer_one_input = page.get_by_role('textbox', name='Answer 1')
        self.answer_two_input = page.get_by_role('textbox', name='Answer 2')
        self.add_new_answer_button = page.get_by_text('Add new Answer')
        self.add_a_question_button = page.get_by_text('Add a Question')
        self.apply_button = page.get_by_text('Apply')
        self.cancel_button = page.get_by_text('Cancel')

    @allure.step('AddAssessmentPage: apply assessment {assessment}')
    def apply_assessment(self, assessment: AssessmentEntity):
        if len(assessment.questions) > 1:
            raise ValueError('Fix this method')
        else:
            self.question_input.fill(assessment.questions[0].question)
            self.answer_one_input.fill(assessment.questions[0].answers[0].answer)
            self.answer_two_input.fill(assessment.questions[0].answers[1].answer)
            self.apply_button.click()
            expect(self.alert_message).to_have_text(assessment_attached_text)
