import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table


class EmailDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.sender_address_text = self.page.locator(
            '//*[contains(@aria-label,"details.senderAddress")]//*[name()="svg"]/following-sibling::p'
        )
        self.date_received = self.page.locator(
            '//*[contains(@aria-label,"details.receivedTime")]//*[name()="svg"]/following-sibling::span'
        )
        self.no_of_employees_received_text = self.page.locator(
            '//*[contains(@aria-label,"details.receivedCount")]//div'
        )
        self.subject_text = self.page.locator(
            '//*[contains(@aria-label,"details.subject")]//div'
        )

        self.email_preview = self.page.get_by_role('tab', name='Email Preview')
        self.employees_received = self.page.get_by_role(
            'tab', name='Employees Received'
        )
        self.links_contained = self.page.get_by_role('tab', name='Links Contained')

    @allure.step('Get email details')
    def get_email_details(self) -> dict:
        return {
            'sender_address': self.sender_address_text.text_content(),
            'date_received': self.date_received.text_content(),
            'no_of_employees_received': self.no_of_employees_received_text.text_content(),
            'subject': self.subject_text.text_content(),
        }


class EmailReceivedTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_input = self.locator.get_by_role('textbox', name='Search by link')
        self.emails_received_table = Table(
            self.locator.locator('.MuiDataGrid-row'), EmailsReceivedTableComponent
        )


class EmailsReceivedTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.email_address_text = self.locator.locator('[data-field="email_address"]')
