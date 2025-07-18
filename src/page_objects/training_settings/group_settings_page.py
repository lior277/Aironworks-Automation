import allure
from playwright.sync_api import Page

from src.models.training_settings.group_settings_config import GroupSettingsConfig
from src.page_objects.training_settings.const import updated_settings_text
from src.page_objects.training_settings.training_settings_page import (
    TrainingSettingsPage,
)


class GroupSettingsPage(TrainingSettingsPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.group_settings_tab = self.page.get_by_role('tab', name='Group Settings')
        self.edit_employees_enable_button = self.page.locator(
            '//p[text()="Edit Employees"]/../..'
        ).get_by_role('button', name='Enabled')
        self.edit_employees_disable_button = self.page.locator(
            '//p[text()="Edit Employees"]/../..'
        ).get_by_role('button', name='Disabled')
        self.launch_campaigns_enable_button = self.page.locator(
            '//p[text()="Launch Campaigns"]/../..'
        ).get_by_role('button', name='Enabled')
        self.launch_campaigns_disable_button = self.page.locator(
            '//p[text()="Launch Campaigns"]/../..'
        ).get_by_role('button', name='Disabled')
        self.read_campaigns_data_enable_button = self.page.locator(
            '//p[text()="Read Campaigns Data"]/../..'
        ).get_by_role('button', name='Enabled')
        self.read_campaigns_data_disable_button = self.page.locator(
            '//p[text()="Read Campaigns Data"]/../..'
        ).get_by_role('button', name='Disabled')
        self.resend_emails_enable_button = self.page.locator(
            '//p[text()="Resend Emails"]/../..'
        ).get_by_role('button', name='Enabled')
        self.resend_emails_disable_button = self.page.locator(
            '//p[text()="Resend Emails"]/../..'
        ).get_by_role('button', name='Disabled')
        self.read_gamification_data_enable_button = self.page.locator(
            '//p[text()="Read Gamification Data"]/../..'
        ).get_by_role('button', name='Enabled')
        self.read_gamification_data_disable_button = self.page.locator(
            '//p[text()="Read Gamification Data"]/../..'
        ).get_by_role('button', name='Disabled')
        self.save_button = self.page.get_by_role('button', name='Save')
        self.discard_button = self.page.get_by_role('button', name='Discard')

    @allure.step('Group Settings: Modify Group Settings')
    def modify_group_settings(self, settings: GroupSettingsConfig):
        if settings.edit_employees_feature:
            self.edit_employees_enable_button.click()
        else:
            self.edit_employees_disable_button.click()
        if settings.launch_campaigns_feature:
            self.launch_campaigns_enable_button.click()
        else:
            self.launch_campaigns_disable_button.click()
        if settings.read_campaigns_data_feature:
            self.read_campaigns_data_enable_button.click()
        else:
            self.read_campaigns_data_disable_button.click()
        if settings.resend_emails_feature:
            self.resend_emails_enable_button.click()
        else:
            self.resend_emails_disable_button.click()
        if settings.read_gamification_data_feature:
            self.read_gamification_data_enable_button.click()
        else:
            self.read_gamification_data_disable_button.click()
        self.save_button.click()
        self.ensure_alert_message_is_visible(updated_settings_text)
