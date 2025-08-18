import allure
from playwright.sync_api import Page, expect


class SupportMenu:
    def __init__(self, page: Page):
        self.page = page
        self.support_menu_button = page.get_by_role('button', name='Open feedback form')
        self.feedback_button = page.get_by_role(
            'button', name='open feedback from menu'
        )
        self.support_chat_button = page.get_by_role('button', name='Open intercom')
        self.feedback_form = page.get_by_role('dialog', name='Feedback Form')
        self.feedback_form_title = self.feedback_form.get_by_role(
            'heading', name='Feedback Form'
        )
        self.feedback_form_text_area = self.feedback_form.get_by_role(
            'textbox', name='Feedback'
        )
        self.feedback_form_cancel_button = self.feedback_form.get_by_role(
            'button', name='Cancel'
        )
        self.feedback_form_submit_button = self.feedback_form.get_by_role(
            'button', name='Submit'
        )
        self.feedback_form_report_id = self.feedback_form.locator(
            '//p[text()="Report ID"]/following-sibling::p'
        ).nth(0)
        self.feedback_form_report_copy_close_button = self.page.get_by_role(
            'button', name='Copy Issue Number and Close'
        )

    @allure.step('SupportMenu: open feedback form')
    def open_feedback_form(self):
        self.support_menu_button.click()
        self.feedback_button.click()
        expect(self.feedback_form).to_be_visible()
        expect(self.feedback_form_title).to_be_visible()
        expect(self.feedback_form_text_area).to_be_visible()
        expect(self.feedback_form_cancel_button).to_be_visible()
        expect(self.feedback_form_submit_button).to_be_visible()

    @allure.step('SupportMenu: submit feedback form')
    def submit_feedback_form(self, feedback: str):
        self.feedback_form_text_area.fill('Test feedback')
        self.feedback_form_submit_button.click()
        # expect(self.feedback_form_report_id).to_be_visible()
        expect(self.feedback_form_report_copy_close_button).to_be_visible()
        self.feedback_form_report_copy_close_button.click()
        expect(self.feedback_form).to_be_hidden()
