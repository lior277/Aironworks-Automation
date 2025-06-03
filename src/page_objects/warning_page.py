from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage


class WarningPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.fill_out_survey_button = self.page.get_by_role(
            'link', name='FILL OUT SURVEY'
        )
        self.learn_phishing_tips_button = self.page.get_by_role(
            'link', name='LEARN PHISHING TIPS'
        )

    def go_to_survey(self):
        with self.page.context.expect_page() as new_page_info:
            self.fill_out_survey_button.click()
        new_page = new_page_info.value
        return SurveyPage(new_page)


class SurveyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.question_sections = self.page.locator(
            '//div[contains(@class, "MuiPaper-root")]'
        )
        self.review_answer_title = self.page.get_by_role(
            'heading', name='Review Answers'
        )
        self.complete_button = self.page.get_by_role('button', name='Complete')
        self.confirm_button = self.page.get_by_role('button', name='Confirm')
        self.edit_button = self.page.get_by_role('button', name='Edit')
        self.thankyou_message = self.page.get_by_role('paragraph')

    def select_radio_option(self, question_number: int, option: int):
        expect(
            self.question_sections.nth(question_number - 1)
            .get_by_role('textbox', name=f'Answer {option}')
            .locator('//following::div//input')
            .nth(0)
        ).to_be_visible()
        self.question_sections.nth(question_number - 1).get_by_role(
            'textbox', name=f'{option}'
        ).locator('//following::div//input').nth(0).click()

    def select_checkbox_option(self, question_number: int, option):
        self.question_sections.nth(question_number + 1).get_by_role(
            'checkbox', name=f'{option}'
        ).click()

    def input_answer(self, question_number: int, answer):
        self.question_sections.nth(question_number + 1).get_by_role(
            'textbox', name='answer'
        ).fill(answer)

    def submit_survey(self):
        self.complete_button.click()
        self.page.wait_for_load_state()
        self.confirm_button.click()
        # assert self.thankyou_message.is_visible()
