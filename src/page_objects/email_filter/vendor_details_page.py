import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.email_filter.const import (
    add_email_domain_to_blocked_list_success_message,
    add_email_domain_to_safe_list_success_message,
    remove_email_domain_from_blocked_list_success_message,
    remove_email_domain_from_safe_list_success_message,
)
from src.page_objects.email_filter.email_details_page import EmailDetailsPage
from src.page_objects.email_filter.sender_details_page import SenderDetailsPage


class VendorDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.vendor_name_text = self.page.get_by_role('heading', level=4)
        self.vendor_url_text = self.page.locator(
            '//*[contains(@aria-label,"vendors.details.vendorUrl")]//*[name()="svg"]/following-sibling::p'
        )
        self.compromised_text = self.page.locator(
            '//*[contains(@aria-label,"vendors.details.compromised")]//div'
        )
        self.no_of_received_emails_text = self.page.locator(
            '//*[contains(@aria-label,"vendors.details.receivedEmails")]//div'
        )
        self.last_received_text = self.page.locator(
            '//*[contains(@aria-label,"details.lastReceived")]//*[name()="svg"]/following-sibling::span'
        )
        self.description_text = self.page.locator(
            '//*[contains(@aria-label,"vendors.details.description")]//div'
        )

        self.employees_received = self.page.get_by_role(
            'tab', name='Employees Received'
        )
        self.associated_senders = self.page.get_by_role(
            'tab', name='Associated Senders'
        )
        self.vendor_domains = self.page.get_by_role('tab', name='Vendor Domains')
        self.vendor_emails = self.page.get_by_role('tab', name='Vendor Emails')

        self.employees_received_tab = EmployeesReceivedTab(
            self.page.get_by_role('tabpanel')
        )
        self.associated_senders_tab = AssociatedSendersTab(
            self.page.get_by_role('tabpanel')
        )
        self.vendor_domains_tab = VendorDomainsTab(self.page.get_by_role('tabpanel'))
        self.vendor_emails_tab = VendorEmailsTab(self.page.get_by_role('tabpanel'))

        self.actions_menu = ActionsMenu(self.page.get_by_role('menu'))

    @allure.step('VendorDetailsPage: Get vendor details')
    def get_vendor_details(self) -> dict:
        self.vendor_name_text.wait_for(state='visible')
        return {
            'vendor_name': self.vendor_name_text.text_content(),
            'vendor_url': self.vendor_url_text.text_content(),
            'no_of_received_emails': self.no_of_received_emails_text.text_content(),
            'last_received': self.last_received_text.text_content(),
            'description': self.description_text.text_content(),
        }

    @allure.step('VendorDetailsPage: Open tab {tab_name}')
    def open_tab(self, tab_name: str):
        match tab_name:
            case 'Employees Received':
                self.employees_received.click()
            case 'Associated Senders':
                self.associated_senders.click()
            case 'Vendor Domains':
                self.vendor_domains.click()
            case 'Vendor Emails':
                self.vendor_emails.click()
            case _:
                raise ValueError(f'Unknown tab name: {tab_name}')
        self.page.wait_for_load_state()

    @allure.step('VendorDetailsPage: Get sender details')
    def get_sender_details(self, sender: str):
        self.open_tab('Associated Senders')
        self.associated_senders_tab.search_sender(sender)
        data = self.associated_senders_tab.get_sender_data()
        return data

    @allure.step('VendorDetailsPage: Go to sender details')
    def go_to_sender_details(self, sender: str):
        self.associated_senders_tab.click_first_row()
        return SenderDetailsPage(self.page)

    @allure.step('VendorDetailsPage: Open sender details')
    def open_sender_details(self, sender: str):
        self.get_sender_details(sender)
        return self.go_to_sender_details(self.page)

    @allure.step('VendorDetailsPage: Get email details')
    def get_vendor_email_details(self, email: str):
        self.open_tab('Vendor Emails')
        self.vendor_emails_tab.search_email(email)
        data = self.vendor_emails_tab.get_email_data()
        return data

    @allure.step('VendorDetailsPage: Go to email details')
    def go_to_vendor_email_details(self):
        self.vendor_emails_tab.click_first_row()
        return EmailDetailsPage(self.page)

    @allure.step('VendorDetailsPage: Open email details')
    def open_vendor_email_details(self, email: str):
        self.get_email_details(email)
        return self.go_to_email_details(self.page)

    @allure.step('VendorDetailsPage: Select sender and block')
    def select_sender_block(self, sender: str):
        self.get_sender_details(sender)
        self.associated_senders_tab.action_first_row()
        self.actions_menu.select_block()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_blocked_list_success_message
        )
        self.associated_senders_tab.senders_table.wait_for_loading()
        data = self.get_sender_details(sender)
        return data

    @allure.step('VendorDetailsPage: Select sender and add to safe list')
    def select_sender_add_to_safe_list(self, email: str):
        self.get_sender_details(email)
        self.associated_senders_tab.action_first_row()
        self.actions_menu.select_add_to_safe_list()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_safe_list_success_message
        )
        self.associated_senders_tab.senders_table.wait_for_loading()
        data = self.associated_senders_tab.get_sender_data()
        return data

    @allure.step('VendorDetailsPage: Select domain and block')
    def select_domain_block(self, domain: str):
        self.open_tab('Vendor Domains')
        self.vendor_domains_tab.action_first_row()
        self.actions_menu.select_block()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_blocked_list_success_message
        )
        self.vendor_domains_tab.domains_table.wait_for_loading()
        data = self.vendor_domains_tab.get_domain_data()
        return data

    @allure.step('VendorDetailsPage: Select domain and add to safe list')
    def select_domain_add_to_safe_list(self, domain: str):
        self.open_tab('Vendor Domains')
        self.vendor_domains_tab.action_first_row()
        self.actions_menu.select_add_to_safe_list()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_safe_list_success_message
        )
        self.vendor_domains_tab.domains_table.wait_for_loading()
        data = self.vendor_domains_tab.get_domain_data()
        return data

    @allure.step('VendorDetailsPage: Select sender and remove from block list')
    def select_sender_remove_from_block_list(self, sender: str):
        self.get_sender_details(sender)
        self.associated_senders_tab.action_first_row()
        self.actions_menu.select_unblock()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_blocked_list_success_message
        )
        self.page.wait_for_load_state(timeout=5)
        data = self.get_sender_details(sender)
        return data

    @allure.step('VendorDetailsPage: Select sender and remove from safe list')
    def select_sender_remove_from_safe_list(self, sender: str):
        self.get_sender_details(sender)
        self.associated_senders_tab.action_first_row()
        self.actions_menu.select_remove_from_safe_list()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_safe_list_success_message
        )
        self.page.wait_for_load_state(timeout=5)
        data = self.get_sender_details(sender)
        return data

    @allure.step('VendorDetailsPage: Select domain and remove from block list')
    def select_domain_remove_from_block_list(self):
        self.open_tab('Vendor Domains')
        self.vendor_domains_tab.action_first_row()
        self.actions_menu.select_unblock()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_blocked_list_success_message
        )
        self.page.wait_for_load_state(timeout=5)
        data = self.vendor_domains_tab.get_domain_data()
        return data

    @allure.step('VendorDetailsPage: Select domain and remove from safe list')
    def select_domain_remove_from_safe_list(self):
        self.open_tab('Vendor Domains')
        self.vendor_domains_tab.action_first_row()
        self.actions_menu.select_remove_from_safe_list()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_safe_list_success_message
        )
        self.page.wait_for_load_state(timeout=5)
        data = self.vendor_domains_tab.get_domain_data()
        return data


class EmployeesReceivedTab(BasePage):
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_input = self.locator.get_by_role(
            'textbox', name='Search by name or email'
        )
        self.emails_received_table = Table(
            self.locator.locator('.MuiDataGrid-row'), EmailsReceivedTableComponent
        )


class EmailsReceivedTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.name = self.locator.locator('[data-field="name"]')
        self.email = self.locator.locator('[data-field="email"]')


class AssociatedSendersTab(BasePage):
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_input = self.locator.get_by_role(
            'textbox', name='Search by name or email'
        )
        self.senders_table = Table(
            self.locator.locator('.MuiDataGrid-row'), AssociatedSendersTableComponent
        )

    def search_sender(self, sender: str):
        self.search_input.fill(sender)
        expect(self.locator.get_by_role('row')).to_have_count(2)

    def get_sender_data(self):
        row = self.senders_table.get_row_by_index(0)
        return row.to_dict()

    def click_first_row(self):
        self.senders_table.get_row_by_index(0).name.click()

    def action_first_row(self):
        self.senders_table.get_row_by_index(0).actions.get_by_role('button').click()


class AssociatedSendersTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.name = self.locator.locator('[data-field="name"]')
        self.email = self.locator.locator('[data-field="email_address"]')
        self.blocked_safe_status = self.locator.locator('[data-field="block_state"]')
        self.actions = self.locator.locator('[data-field="actions"]')

    def to_dict(self):
        return {
            'sender_name': self.name.text_content(),
            'sender_domain': self.email.text_content().split('@')[1].strip(),
            'blocked_safe_status': self.blocked_safe_status.text_content(),
        }


class VendorDomainsTab(BasePage):
    def __init__(self, locator: Locator):
        self.locator = locator
        self.domains_table = Table(
            self.locator.locator('.MuiDataGrid-row'), VendorDomainsTableComponent
        )

    def get_domain_data(self):
        row = self.domains_table.get_row_by_index(0)
        return row.to_dict()

    def action_first_row(self):
        self.domains_table.get_row_by_index(0).actions.get_by_role('button').click()


class VendorDomainsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.domain = self.locator.locator('[data-field="domain"]')
        self.blocked_safe_status = self.locator.locator('[data-field="block_state"]')
        self.actions = self.locator.locator('[data-field="actions"]')

    def to_dict(self):
        return {
            'domain': self.domain.text_content(),
            'blocked_safe_status': self.blocked_safe_status.text_content(),
        }


class VendorEmailsTab(BasePage):
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_input = self.locator.get_by_role('textbox', name='Search by Email')
        self.emails_table = Table(
            self.locator.locator('.MuiDataGrid-row'), VendorEmailsTableComponent
        )

    def search_email(self, email: str):
        self.search_input.fill(email)

    def get_email_data(self):
        row = self.emails_table.get_row_by_index(0)
        return row.to_dict()

    def click_first_row(self):
        self.emails_table.get_row_by_index(0).date_received.click()


class VendorEmailsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.date_received = self.locator.locator('[data-field="received_time"]')
        self.subject = self.locator.locator('[data-field="subject"]')
        self.risk_level = self.locator.locator('[data-field="verdict"]')

    def to_dict(self):
        return {
            'date_received': self.date_received.text_content(),
            'subject': self.subject.text_content(),
        }


class ActionsMenu:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.block_option = self.locator.get_by_role('menuitem', name='Block')
        self.add_to_safe_list_option = self.locator.get_by_role(
            'menuitem', name='Add to safe list'
        )
        self.unblock_option = self.locator.get_by_role('menuitem', name='Unblock')
        self.remove_from_safe_list_option = self.locator.get_by_role(
            'menuitem', name='Remove from safe list'
        )

    def select_block(self):
        self.block_option.scroll_into_view_if_needed()
        self.block_option.click()

    def select_add_to_safe_list(self):
        self.add_to_safe_list_option.scroll_into_view_if_needed()
        self.add_to_safe_list_option.click()

    def select_unblock(self):
        self.unblock_option.scroll_into_view_if_needed()
        self.unblock_option.click()

    def select_remove_from_safe_list(self):
        self.remove_from_safe_list_option.scroll_into_view_if_needed()
        self.remove_from_safe_list_option.click()
