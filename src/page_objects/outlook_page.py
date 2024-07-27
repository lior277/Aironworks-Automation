import re
import time
from typing import Literal

import allure
from playwright.sync_api import Page, expect
from src.configs.config_loader import AppConfigs


class OutlookPage:
    def __init__(self, page: Page):
        self.page = page

        self.mail_icon = page.locator('#avatar-rq span')
        self.apps_locator = page.get_by_label('Apps', exact=True)
        self.app_frame = page.frame_locator(
            f'iframe[src^="{AppConfigs.ADDIN_BASE_URL}"]'
        )
        self.perform_assessment_button = self.app_frame.get_by_role(
            'button', name='Perform Assessment'
        )
        self.report_incident_button = self.app_frame.get_by_role(
            'button', name='Report an Incident'
        )

    @allure.step('OutlookPage: login to outlook')
    def login(self):
        self.page.goto('https://outlook.office.com/mail/')
        self.page.fill('[name="loginfmt"]', AppConfigs.MSLIVE_USER)
        self.page.click('[type="submit"]')

        self.page.fill('input[type="password"]', AppConfigs.MSLIVE_PWD)
        self.page.get_by_role('button', name='Sign in').click()
        self.page.get_by_role('button', name='Yes').click()
        self.page.get_by_role('treeitem', name='Inbox', exact=True).click()

    @allure.step('OutlookPage: goto message id')
    def goto_message(self, message_id: str):
        self.page.goto(f'https://outlook.office.com/mail/inbox/id/{message_id}')
        self.mail_icon.click()

    @allure.step('OutlookPage: open addin')
    def open_addin(self):
        self.apps_locator.wait_for(timeout=10000)
        expect(self.apps_locator).to_be_visible()
        self.apps_locator.click()
        self.page.get_by_label(AppConfigs.ADDIN_NAME, exact=True).click()

    @allure.step('OutlookPage: perform assessment')
    def perform_assessment(self):
        self.perform_assessment_button.click()

    @allure.step('OutlookPage: report incident')
    def report_incident(self):
        self.report_incident_button.click()
