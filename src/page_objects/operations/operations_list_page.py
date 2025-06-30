from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.operations.create_operation_page import CreateOperationPage
from src.page_objects.operations.operation_detail_page import OperationDetailPage


class OperationsListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_operation_button = self.page.get_by_role(
            'button', name='Create Operation'
        )
        self.operations_table = Table(
            self.page.locator('.MuiDataGrid-row'), OperationsTableComponent
        )

    def navigate_to_create_operation_page(self):
        self.create_operation_button.click()
        return CreateOperationPage(self.page)

    def navigate_to_first_operation_page(self):
        row = self.operations_table.get_row_by_index(0)
        if not row:
            raise ValueError('Table is empty')
        row.name.click()
        return OperationDetailPage(self.page)


class OperationsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.name = self.locator.locator('[data-field="name"]')
        self.start_date = self.locator.locator('[data-field="start_date"]')
        self.end_date = self.locator.locator('[data-field="end_date"]')
        self.created_date = self.locator.locator('[data-field="date_created"]')
        self.actions = self.locator.locator('[data-field="actions"]')

    def to_dict(self):
        return {
            'name': self.name.text_content(),
            'start_date': self.start_date.text_content(),
            'end_date': self.end_date.text_content(),
            'created_date': self.created_date.text_content(),
        }
