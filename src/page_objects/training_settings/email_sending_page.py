from playwright.sync_api import Page

from src.page_objects.training_settings.const import updated_settings_text
from src.page_objects.training_settings.training_settings_page import (
    TrainingSettingsPage,
)


class EmailSendingPage(TrainingSettingsPage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_header_settings_section = self.page.locator(
            '//p[text()="Email Header Settings"]//ancestor::div[contains(@class,"MuiPaper")]'
        )
        self.email_header_settings_enable_button = (
            self.email_header_settings_section.get_by_role('button', name='Enabled')
        )
        self.email_header_settings_disable_button = (
            self.email_header_settings_section.get_by_role('button', name='Disabled')
        )
        self.header_key_input = self.email_header_settings_section.get_by_role(
            'textbox', name='Header Key'
        )
        self.header_value_input = self.email_header_settings_section.get_by_role(
            'textbox', name='Header Value'
        )

    def enable_email_header_settings(self, header_key: str, header_value: str):
        self.email_header_settings_enable_button.scroll_into_view_if_needed()
        self.email_header_settings_enable_button.click()
        self.header_key_input.wait_for()
        self.header_value_input.wait_for()
        self.header_key_input.fill(header_key)
        self.header_value_input.fill(header_value)
        self.save_changes()
        self.ensure_alert_message_is_visible(updated_settings_text)

    def disable_email_header_settings(self):
        self.header_key_input.fill('abc')
        self.header_value_input.fill('')
        self.email_header_settings_disable_button.click()
        self.save_changes()
        self.ensure_alert_message_is_visible(updated_settings_text)
