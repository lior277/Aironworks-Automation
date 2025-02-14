from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table


class PreviousPhishingSimulationsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_breadcrumbs = self.page.get_by_role('link', name='Dashboard')
        self.back_button = self.page.get_by_role('button', name='Back')
        self.previous_phishing_simulations_table = Table(
            self.page.locator('//*[contains(@class,"MuiDataGrid-row")]'),
            PreviousPhishingSimulationsTableComponent,
        )
        self.previous_phishing_simulations_preview_popup = self.page.get_by_role(
            'dialog'
        )

    def click_preview_first_row(self):
        self.previous_phishing_simulations_table.wait_for_loading()
        row = self.previous_phishing_simulations_table.get_row_by_index(0)
        if not row:
            raise Exception('No rows found in the table')
        row.click_preview_button()

    def get_first_row_data(self):
        self.previous_phishing_simulations_table.wait_for_loading()
        row = self.previous_phishing_simulations_table.get_row_by_index(0)
        if not row:
            raise Exception('No rows found in the table')
        return row.to_dict()


class PreviousPhishingSimulationsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('[data-field="strategy_name"]')
        self.status = self.locator.locator('[data-field="status"]')
        self.sent_date = self.locator.locator('[data-field="mail_request_send"]')
        self.action_button = self.locator.locator('[data-field="actions"]')

    def to_dict(self):
        return {
            'title': self.title.text_content(),
            'status': self.status.text_content(),
            'sent_date': self.sent_date.text_content(),
            'action_button': self.action_button.text_content(),
        }

    def click_preview_button(self):
        self.action_button.get_by_role('button', name='Preview').click()


class PreviewDialog:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading')

    def get_title(self):
        return self.title.text_content()
