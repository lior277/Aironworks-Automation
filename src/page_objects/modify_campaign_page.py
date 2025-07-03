from datetime import datetime, timedelta

from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.const import modify_campaign_successfully_text
from src.page_objects.data_types.filter import Filter


class ModifyCampaignPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.bread_crumb = self.page.get_by_label('current-breadcrumb')
        self.back_button = self.page.get_by_role('button', name='Back')
        self.save_button = self.page.get_by_role('button', name='Save')
        self.show_filters_button = self.page.get_by_role('button', name='Show filters')
        self.completion_date_textbox = self.page.get_by_role(
            'textbox', name='Completion date'
        )
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.locator('select', has_text='Email'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
        )
        self.employee_checkbox = self.page.get_by_role('checkbox', name='Select row')

    def filter_by_email(self, email: str):
        self.filter.filter_by('email', email)
        self.wait_for_loading_state()
        self.bread_crumb.hover()

    def edit_campaign(self, email: str):
        self.fill_completion_date()
        self.filter_by_email(email)
        self.employee_checkbox.check()
        self.save_button.click()
        expect(self.alert_message).to_have_text(modify_campaign_successfully_text)

    def fill_completion_date(self):
        now = datetime.now()
        future_date = now + timedelta(days=2)
        formatted_date = future_date.strftime('%m/%d/%Y %I:%M %p').lower()
        self.completion_date_textbox.fill(formatted_date)
