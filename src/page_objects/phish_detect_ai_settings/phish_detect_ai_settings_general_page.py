from playwright.sync_api import Page

from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_page import (
    PhishDetectAISettings,
)


class PhishDetectAISettingsGeneral(PhishDetectAISettings):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = self.page.get_by_label('Email address').first
