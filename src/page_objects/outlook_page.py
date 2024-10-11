from time import sleep

import allure
import pyotp
from playwright.sync_api import Page, expect

from src.configs.config_loader import AppConfigs


class OutlookPage:
    def __init__(self, page: Page):
        self.page = page

        self.mail_icon = page.locator('[data-testid="SentReceivedSavedTime"]')
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
        self.login_button = self.app_frame.get_by_role('button', name='Login')
        self.allow_button = self.app_frame.get_by_role('button', name='Allow')
        self.addin_name_button = self.page.get_by_label(
            AppConfigs.ADDIN_NAME, exact=True
        ).first

    @allure.step('OutlookPage: login to outlook')
    def login(self):
        self.page.goto('https://outlook.office.com/mail/')
        self.page.fill('[name="loginfmt"]', AppConfigs.MSLIVE_USER)
        self.page.click('[type="submit"]')

        self.page.fill('input[type="password"]', AppConfigs.MSLIVE_PWD)
        self.page.locator('[data-report-event="Signin_Submit"]').click()
        self.page.locator('[type="submit"]').click()
        if self.page.locator('input[type="tel"]').is_visible(timeout=10000):
            self.verify_login()
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
    def goto_message(self, message_id: str):
        self.page.goto(f'https://outlook.office.com/mail/inbox/id/{message_id}')
        self.mail_icon.last.click()

    @allure.step('OutlookPage: open addin')
    def open_addin(self):
        self.apps_locator.wait_for(timeout=10000)
        expect(self.apps_locator).to_be_visible()
        self.apps_locator.click()
        sleep(2)  # just to make sure all apps were displayed
        self.addin_name_button.wait_for()
        self.addin_name_button.click()
        self.login_addin()

    @allure.step('OutlookPage: perform assessment')
    def login_addin(self):
        self.login_button.click()
        self.allow_button.click()
        self.perform_assessment_button.wait_for()

    @allure.step('OutlookPage: perform assessment')
    def perform_assessment(self):
        self.perform_assessment_button.click()

    @allure.step('OutlookPage: report incident')
    def report_incident(self):
        self.report_incident_button.click()
