import re

import allure
from playwright.sync_api import FrameLocator, Page, expect


class EducationLandingPage:
    def __init__(self, page: Page, link_url: str):
        self.page = page
        self.email_input = self.page.get_by_role('textbox', name='email')
        self.submit_button = self.page.get_by_role('button', name='Submit')
        self.complete_button = self.page.get_by_role('button', name='Complete')
        self.embedded_content: FrameLocator = self.page.frame_locator('iframe')
        self.link_url = link_url

    @property
    def iframe(self):
        return self.embedded_content.owner

    @allure.step('EducationLandingPage: open page')
    def open(self):
        self.page.goto(self.link_url)
        self.page.wait_for_load_state('load')

    @allure.step('EducationLandingPage: submit email')
    def submit_email(self, email: str):
        expect(self.email_input).to_be_visible()
        self.email_input.fill(email)

        expect(self.submit_button).to_be_visible()
        with self.page.expect_request_finished():
            self.submit_button.click()

        expect(self.embedded_content.owner).to_be_visible()
        expect(self.embedded_content.owner).to_have_attribute(
            'src', re.compile('https://.*')
        )
