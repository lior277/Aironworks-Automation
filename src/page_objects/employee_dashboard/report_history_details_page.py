from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table


class ReportHistoryDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_breadcrumbs = self.page.get_by_role('link', name='Dashboard')
        self.back_button = self.page.get_by_role('button', name='Back')
        self.report_history_details_table = Table(
            self.page.locator('//*[contains(@class,"MuiDataGrid-row")]'),
            ReportHistoryDetailsTableComponent,
        )

    def get_first_row_data(self):
        self.report_history_details_table.wait_for_loading()
        row = self.report_history_details_table.get_row_by_index(0)
        if not row:
            raise Exception('No rows found in the table')
        return row.to_dict()


class ReportHistoryDetailsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.report_type = self.locator.locator('[data-field="kind"]')
        self.date_submitted = self.locator.locator('[data-field="date_created"]')
        self.sender_email = self.locator.locator('[data-field="sender"]')
        self.subject = self.locator.locator('[data-field="subject"]')
        self.risk_level = self.locator.locator('[data-field="level"]')
        self.status = self.locator.locator('[data-field="status"]')

    def to_dict(self):
        return {
            'report_type': self.report_type.text_content(),
            'date_submitted': self.date_submitted.text_content(),
            'sender_email': self.sender_email.text_content(),
            'subject': self.subject.text_content(),
            'risk_level': self.risk_level.text_content(),
            'status': self.status.text_content(),
        }
