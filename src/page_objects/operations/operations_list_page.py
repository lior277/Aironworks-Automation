from playwright.sync_api import Page

from src.page_objects.base_page import BasePage
from src.page_objects.operations.create_operation_page import CreateOperationPage


class OperationsListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_operation_button = self.page.get_by_role(
            'button', name='Create Operation'
        )

    def navigate_to_create_operation_page(self):
        self.create_operation_button.click()
        return CreateOperationPage(self.page)
