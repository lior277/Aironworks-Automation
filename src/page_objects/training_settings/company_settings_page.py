from playwright.sync_api import Page

from src.page_objects.training_settings.training_settings_page import (
    TrainingSettingsPage,
)


class CompanySettingsPage(TrainingSettingsPage):
    def __init__(self, page: Page):
        super().__init__(page)
