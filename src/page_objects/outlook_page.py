import random
import string
from datetime import datetime
from time import sleep

import allure
import pyotp
from playwright._impl._errors import TargetClosedError
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.configs.config_loader import AppConfigs


class OutlookPage:
    def __init__(self, page: Page):
        self.page = page

        self.mail_icon = page.get_by_role('option')
        self.apps_locator = page.get_by_label('Apps', exact=True)
        self.app_frame = page.frame_locator(
            f'iframe[src^="{AppConfigs.ADDIN_BASE_URL}"]'
        )
        self.perform_assessment_button = self.app_frame.get_by_role(
            'button', name='Perform AI Risk Assessment'
        )
        self.report_incident_button = self.app_frame.get_by_role(
            'button', name='Report an Incident'
        )
        self.report_description = self.app_frame.get_by_role(
            'textbox', name='Add a description of what happened'
        )
        self.report_incident_submit_button = self.app_frame.get_by_role(
            'button', name='Submit'
        )
        self.report_incident_cancel_button = self.app_frame.get_by_role(
            'button', name='Cancel'
        )
        self.login_button = self.app_frame.get_by_role('button', name='Login')
        self.allow_button = self.app_frame.get_by_role('button', name='Allow')
        self.addin_name_button = self.page.get_by_label(
            AppConfigs.ADDIN_NAME, exact=True
        ).first
        self.search_mail_input = self.page.locator('//input[@id="topSearchInput"]')
        self.search_button = self.page.get_by_role('button', name='Search', exact=True)

    @allure.step('OutlookPage: go to outlook')
    def go_to_outlook(self):
        self.page.goto('https://outlook.office.com/mail/')

    @allure.step('OutlookPage: login to outlook')
    def login(self):
        self.page.fill('[name="loginfmt"]', AppConfigs.MSLIVE_USER)
        self.page.click('[type="submit"]')

        self.page.fill('input[type="password"]', AppConfigs.MSLIVE_PWD)
        self.page.locator('[data-report-event="Signin_Submit"]').click()
        self.page.locator('[type="submit"]').click()
        try:
            self.page.wait_for_selector(
                'input[type="tel"]', timeout=10000, strict=False
            )
            if self.page.locator('input[type="tel"]').is_visible(timeout=10000):
                self.verify_login()
        except (TargetClosedError, PlaywrightTimeoutError):
            print('No verification code needed. Proceeding...')

    @allure.step('OutlookPage: navigate to inbox')
    def navigate_to_inbox(self):
        self.page.locator(
            '[aria-labelledby="favoritesRoot"] [data-folder-name="inbox"]'
        ).click()

    def verify_login(self):
        totp = pyotp.TOTP(AppConfigs.MSLIVE_TOTP)
        self.page.fill('input[type="tel"]', totp.now())
        self.page.click('[type="submit"]')
        if self.page.locator('[name="Yes"]').is_visible(timeout=10000):
            self.page.locator('[name="Yes"]').click()

    @allure.step('OutlookPage: goto message id')
    def goto_message(self, message: str):
        self.search_mail_input.fill(message)
        self.search_button.click()
        self.mail_icon.first.click()

    @allure.step('OutlookPage: open addin')
    def open_addin(self):
        self.apps_locator.wait_for(timeout=10000)
        expect(self.apps_locator).to_be_visible()
        self.apps_locator.click()
        sleep(2)  # just to make sure all apps were displayed
        self.addin_name_button.wait_for()
        self.addin_name_button.click()
        try:
            self.login_button.wait_for(timeout=10000)
            if self.login_button.is_visible(timeout=10000):
                self.login_addin()
        except PlaywrightTimeoutError:
            print('Addin already logged in')

    @allure.step('OutlookPage: perform assessment')
    def login_addin(self):
        self.login_button.click()
        # self.allow_button.click()
        self.perform_assessment_button.wait_for()

    @allure.step('OutlookPage: perform assessment')
    def perform_assessment(self):
        self.perform_assessment_button.click()

    @allure.step('OutlookPage: report incident')
    def report_incident(self):
        random_description = (
            f'Description: {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} '
        )
        f'{"".join(random.choices(string.ascii_lowercase + string.digits, k=8))}'

        self.report_incident_button.click()
        # Generate Random description
        self.report_description.fill(random_description)
        self.report_incident_submit_button.click()
