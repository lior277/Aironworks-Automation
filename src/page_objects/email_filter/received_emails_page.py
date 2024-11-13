import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.data_types.table_element import Table
from src.page_objects.email_filter.const import TabName
from src.page_objects.email_filter.sender_details_page import SenderDetailsPage


class ReceivedEmailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.high_risk_emails = self.page.get_by_role('tab', name='High Risk Emails')
        self.senders = self.page.get_by_role('tab', name='Senders')
        self.vendors = self.page.get_by_role('tab', name='Vendors')

        self.high_risk_emails_tab = HighRiskEmailsTab(self.page.get_by_role('tabpanel'))
        self.senders_tab = SendersTab(self.page.get_by_role('tabpanel'))
        self.vendors_tab = VendorsTab(self.page.get_by_role('tabpanel'))

    @allure.step('ReceivedEmailsPage: open high risk emails list')
    def open_tab(self, tab_name: str):
        match tab_name:
            case TabName.HIGH_RISK_EMAILS:
                self.high_risk_emails.click()
            case TabName.SENDERS_LIST:
                self.senders.click()
            case TabName.VENDORS_LIST:
                self.vendors.click()
            case _:
                raise ValueError(f'Tab {tab_name} is not supported')

    @allure.step('ReceivedEmailsPage: open senders details of {email}')
    def open_senders_details(self, email: str, employee: str = None):
        self.get_senders(email, employee)
        return self.go_to_senders_details(email)

    @allure.step('ReceivedEmailsPage: get senders')
    def get_senders(self, email, employee: str = None):
        self.senders.click()
        if employee:
            self.senders_tab.open_tab('Employee', employee)
            self.page.wait_for_load_state(timeout=5)
        self.senders_tab.search_by_email(email)
        self.page.wait_for_load_state(timeout=5)
        return self.senders_tab.get_senders()

    @allure.step('ReceivedEmailsPage: go to senders details')
    def go_to_senders_details(self, email: str):
        self.senders_tab.click_by_email(email)
        return SenderDetailsPage(self.page)


class HighRiskEmailsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        # High risk emails table
        self.table = Table(
            self.locator.locator('.MuiDataGrid-row'), HighRiskEmailsTableComponent
        )


class HighRiskEmailsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.sender_address = self.locator.locator('[data-field="sender_address"]')
        self.date_received = self.locator.locator('[data-field="received_time"]')
        self.no_of_employees_received = self.locator.locator(
            '[data-field="received_count"]'
        )
        self.attachment = self.locator.locator('[data-field="has_attachment"]')
        self.subject = self.locator.locator('[data-field="subject"]')


class SendersTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.company = self.locator.get_by_role('tab', name='Company')
        self.employee = self.locator.get_by_role('tab', name='Employee')

        self.email_search = self.locator.get_by_role('textbox', name='Search by email')

        # Company tab
        self.company_table = Table(
            self.locator.locator('.MuiDataGrid-row'), SendersTableComponent
        )

        # Employee tab

        self.employee_dropdown = DropDown(
            self.locator.get_by_role('combobox', name='Employee'),
            option_list_locator=self.locator.get_by_role('option'),
        )
        self.employee_table = Table(
            self.locator.locator('.MuiDataGrid-row'), SendersTableComponent
        )

    def open_tab(self, tab_name: str, employee: str = None):
        match tab_name:
            case 'Company':
                self.company.click()
            case 'Employee':
                self.employee.click()
                self.employee_dropdown.select_item_by_text(employee)
            case _:
                raise ValueError(f'Tab {tab_name} is not supported')

    def search_by_email(self, email: str):
        self.email_search.fill(email)

    def click_by_email(self, email: str):
        self.search_by_email(email)
        row = self.company_table.get_row_by_column_value('email_address', email)
        if not row:
            raise ValueError(f'Unable to find email {email}')
        row.email_address.click()

    def get_senders(self):
        return self.company_table.text_content()


class SendersTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.sender_name = self.locator.locator('[data-field="name"]')
        self.email_address = self.locator.locator('[data-field="email_address"]')
        self.highest_risk_level = self.locator.locator(
            '[data-field="risk_details.max_risk_level"]'
        )
        self.average_risk_level = self.locator.locator(
            '[data-field="risk_details.average_risk_level"]'
        )
        self.no_of_emails_received = self.locator.locator(
            '[data-field="total_mails_received"]'
        )
        self.no_of_employees_received = self.locator.locator(
            '[data-field="total_number_of_employees"]'
        )
        self.blocked_safe_status = self.locator.locator('[data-field="block_state"]')
        self.first_contact = self.locator.locator('[data-field="first_received_time"]')
        self.last_contact = self.locator.locator('[data-field="last_received_time"]')


class VendorsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.vendors_table = Table(
            self.locator.locator('.MuiDataGrid-row'), VendorsTableComponent
        )


class VendorsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.vendor_name = self.locator.locator('[data-field="name"]')
        self.compromised = self.locator.locator('[data-field="is_compromised"]')
        self.vendor_url_site = self.locator.locator('[data-field="url"]')
        self.description = self.locator.locator('[data-field="description"]')
        self.no_of_emails_received = self.locator.locator(
            '[data-field="total_mails_received"]'
        )
        self.last_received = self.locator.locator('[data-field="last_received_time"]')
