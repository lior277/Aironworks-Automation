from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class TrainingSettingsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.company_settings = self.page.get_by_role('tab', name='Company Settings')
        self.notifications_for_employees = self.page.get_by_role(
            'tab', name='Notifications For Employees'
        )
        self.email_sending = self.page.get_by_role('tab', name='Email Sending')
        self.warning = self.page.get_by_role('tab', name='Warning')
        self.save_button = self.page.get_by_role('button', name='Save')
        self.discard_button = self.page.get_by_role('button', name='Discard')

    def select_tab(self, tab_name: str):
        match tab_name:
            case 'Company Settings':
                self.company_settings.click()
                self.wait_for_progress_bar_disappears()
            case 'Notifications For Employees':
                self.notifications_for_employees.click()
                self.wait_for_progress_bar_disappears()
            case 'Email Sending':
                self.email_sending.click()
                self.wait_for_progress_bar_disappears()
            case 'Warning':
                self.warning.click()
                self.wait_for_progress_bar_disappears()
            case _:
                raise ValueError(f'Unknown tab name: {tab_name}')

    def save_changes(self):
        self.save_button.click()
