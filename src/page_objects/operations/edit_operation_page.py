from playwright.sync_api import Page, expect

from src.models.operation_model import OperationModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.filter import Filter
from src.page_objects.operations.const import edit_successful_text


class EditOperationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.bread_crumb = self.page.get_by_label('current-breadcrumb')
        self.cancel_button = self.page.get_by_text('Cancel')
        self.save_button = self.page.get_by_role('button', name='Save')
        self.operation_name_input = self.page.get_by_role(
            'textbox', name='Operation Name'
        )
        self.show_filters_button = self.page.get_by_role('button', name='Show filters')
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.locator('select', has_text='Campaign Name'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
        )
        self.campaign_checkbox = self.page.get_by_role('checkbox', name='Select row')

    def edit_operation(self, operation: OperationModel):
        print(f'Edit operation: {operation.operation_name}')
        self.operation_name_input.fill(operation.operation_name)
        self.filter_campaign_by_name(operation.campaign_name)
        self.campaign_checkbox.check()
        self.save_button.click()
        expect(self.alert_message).to_have_text(edit_successful_text)

    def filter_campaign_by_name(self, campaign_name: str):
        self.filter.filter_by('campaign_name', campaign_name)
        self.wait_for_loading_state()
        self.bread_crumb.hover()
