from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.operations.const import delete_successful_text
from src.page_objects.operations.edit_operation_page import EditOperationPage


class OperationDetailPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.breadcrumb = self.page.get_by_role('current-breadcrumb')
        self.name = self.page.get_by_label('operations.list.table.name').locator('/div')
        self.start_date = self.page.get_by_label(
            'operations.list.table.start_date'
        ).locator('/div')
        self.end_date = self.page.get_by_label(
            'operations.list.table.end_date'
        ).locator('/div')
        self.created_date = self.page.get_by_label(
            'operations.list.table.created_date'
        ).locator('/div')

        self.back_button = self.page.get_by_role('button', name='Back')
        self.edit_button = self.page.get_by_role('button', name='Edit')
        self.delete_button = self.page.get_by_role('button', name='Delete')

        self.confirm_delete_dialog = self.page.get_by_role(
            'dialog', name='Confirm Deleting'
        )

    def navigate_to_edit_operation_page(self):
        self.edit_button.click()
        return EditOperationPage(self.page)

    def delete_operation(self):
        self.delete_button.click()
        self.confirm_delete_dialog.wait_for()
        self.confirm_delete_dialog.get_by_role('button', name='Delete').click()
        expect(self.alert_message).to_have_text(delete_successful_text)
