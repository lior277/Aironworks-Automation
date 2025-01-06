import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.data_types.table_element import Table
from src.page_objects.email_filter.const import TabName
from src.page_objects.email_filter.email_details_page import EmailDetailsPage
from src.page_objects.email_filter.sender_details_page import SenderDetailsPage
from src.page_objects.email_filter.vendor_details_page import VendorDetailsPage


class ReceivedEmailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.high_risk_emails = self.page.get_by_role('tab', name='High-Risk Emails')
        self.senders = self.page.get_by_role('tab', name='Senders')
        self.vendors = self.page.get_by_role('tab', name='Vendors')

        self.high_risk_emails_tab = HighRiskEmailsTab(self.page.get_by_role('tabpanel'))
        self.senders_tab = SendersTab(self.page.get_by_role('tabpanel'))
        self.vendors_tab = VendorsTab(self.page.get_by_role('tabpanel'))

    @allure.step('ReceivedEmailsPage: open tab {tab_name}')
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
        self.page.wait_for_load_state(timeout=5)

    @allure.step('ReceivedEmailsPage: open senders details of {email}')
    def open_senders_details(self, email: str, employee: str = None):
        self.get_sender(email, employee)
        return self.go_to_senders_details(email)

    @allure.step('ReceivedEmailsPage: get sender')
    def get_sender(self, email, employee: str = None):
        self.open_tab('Senders')
        if employee:
            self.senders_tab.open_tab('Employee', employee)
            self.page.wait_for_load_state(timeout=5)
        self.senders_tab.search_by_email(email)
        data = self.senders_tab.get_sender_data()
        return data

    @allure.step('ReceivedEmailsPage: go to senders details')
    def go_to_senders_details(self, email: str):
        self.senders_tab.click_by_email(email)
        return SenderDetailsPage(self.page)

    @allure.step('ReceivedEmailsPage: open high risk email details of first email')
    def open_high_risk_email_details(self):
        self.get_high_risk_email()
        return self.go_to_high_risk_email_details()

    @allure.step('ReceivedEmailsPage: get high risk email')
    def get_high_risk_email(self):
        self.open_tab('High-Risk Emails')
        data = self.high_risk_emails_tab.get_email_data()
        return data

    @allure.step('ReceivedEmailsPage: go to high risk email details')
    def go_to_high_risk_email_details(self):
        self.high_risk_emails_tab.click_first_row()
        return EmailDetailsPage(self.page)

    @allure.step('ReceivedEmailsPage: open vendor details of {vendor}')
    def open_vendor_details(self, vendor: str):
        self.get_vendor(vendor)
        return self.go_to_vendor_details(vendor)

    @allure.step('ReceivedEmailsPage: get vendor')
    def get_vendor(self, vendor: str):
        self.open_tab('Vendors')
        self.vendors_tab.search_by_vendor_name_domain(vendor)
        data = self.vendors_tab.get_vendor_data()
        return data

    @allure.step('ReceivedEmailsPage: go to vendor details')
    def go_to_vendor_details(self, vendor: str):
        self.vendors_tab.click_by_vendor_name(vendor)
        return VendorDetailsPage(self.page)


class HighRiskEmailsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        # High risk emails table
        self.high_risk_emails_table = Table(
            self.locator.locator('.MuiDataGrid-row'), HighRiskEmailsTableComponent
        )

    def get_email_data(self):
        row = self.high_risk_emails_table.get_row_by_index(0)
        return row.to_dict()

    def click_first_row(self):
        row = self.high_risk_emails_table.get_row_by_index(0)
        if not row:
            raise ValueError('Table is empty')
        row.sender_address.click()


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

    def to_dict(self):
        return {
            'sender_address': self.sender_address.text_content().strip(),
            'date_received': self.date_received.text_content(),
            'no_of_employees_received': self.no_of_employees_received.text_content(),
            'subject': self.subject.text_content(),
        }


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
        self.company_table.get_row_by_index(0).email_address.filter(
            has_text=email
        ).wait_for()

    def click_by_email(self, email: str):
        self.search_by_email(email)
        row = self.company_table.get_row_by_column_value('email_address', email)
        if not row:
            raise ValueError(f'Unable to find email {email}')
        row.email_address.click()

    def get_sender_data(self):
        row = self.company_table.get_row_by_index(0)
        return row.to_dict()


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

    def to_dict(self):
        if self.sender_name.text_content() == 'Sender Name Unavailable':
            sender_name_text = ' '
        else:
            sender_name_text = self.sender_name.text_content()
        return {
            'sender_name': sender_name_text.strip(),
            'sender_domain': self.email_address.text_content().split('@')[1].strip(),
            'first_contacted': self.first_contact.text_content(),
            'last_received': self.last_contact.text_content(),
            'no_of_emails_received': self.no_of_emails_received.text_content(),
            'no_of_employees_received': self.no_of_employees_received.text_content(),
            'highest_risk_level': self.highest_risk_level.text_content(),
            'average_risk_level': self.average_risk_level.text_content(),
            'blocked_safe_status': self.blocked_safe_status.text_content(),
        }


class VendorsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_input = self.locator.get_by_role(
            'textbox', name='Search by vendor name or domain'
        )
        self.vendors_table = Table(
            self.locator.locator('.MuiDataGrid-row'), VendorsTableComponent
        )

    def search_by_vendor_name_domain(self, search_text: str):
        self.search_input.fill(search_text)
        self.vendors_table.get_row_by_index(0).vendor_name.filter(
            has_text=search_text
        ).wait_for()

    def click_by_vendor_name(self, vendor_name: str):
        # self.search_by_vendor_name_domain(vendor_name)
        row = self.vendors_table.get_row_by_column_value('vendor_name', vendor_name)
        if not row:
            raise ValueError(f'Unable to find vendor {vendor_name}')
        row.vendor_name.click()

    def get_vendor_data(self):
        row = self.vendors_table.get_row_by_index(0)
        return row.to_dict()


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

    def to_dict(self):
        return {
            'vendor_name': self.vendor_name.text_content().strip(),
            'vendor_url': self.vendor_url_site.text_content(),
            'description': self.description.text_content(),
            'no_of_received_emails': self.no_of_emails_received.text_content(),
            'last_received': self.last_received.text_content(),
        }
