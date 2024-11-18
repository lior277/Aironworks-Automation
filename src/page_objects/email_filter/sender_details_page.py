import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.email_filter.const import (
    add_email_domain_to_blocked_list_success_message,
    add_email_domain_to_safe_list_success_message,
)


class SenderDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.add_to_block_list_button = self.page.get_by_role('button', name='Block')
        self.add_to_safe_list_button = self.page.get_by_role(
            'button', name='Add to safe list'
        )
        self.unblock_button = self.page.get_by_role('button', name='Unblock')
        self.remove_from_safe_list_button = self.page.get_by_role(
            'button', name='Remove from safe list'
        )
        self.sender_domain_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.domain")]//*[name()="svg"]/..'
        )
        self.first_contacted_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.firstContact")]//*[name()="svg"]/following-sibling::span'
        )
        self.last_received_text = self.page.locator(
            '//*[contains(@aria-label,"details.lastReceived")]//*[name()="svg"]/following-sibling::span'
        )
        self.no_of_emails_received_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.receivedEmails")]//div'
        )
        self.no_of_employees_received_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.numOfEmployees")]//div'
        )
        self.highest_risk_level_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.highestRiskLevel")]//descendant::div[last()]'
        )
        self.average_risk_level_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.averageRiskLevel")]//descendant::div[last()]'
        )
        self.blocked_safe_status_text = self.page.locator(
            '//*[contains(@aria-label,"senders.details.blockedSafeStatus")]//descendant::div[last()]'
        )
        self.sender_emails = self.page.get_by_role('tab', name='Sender Emails')
        self.no_of_employees_received = self.page.get_by_role(
            'tab', name='Emails Received'
        )
        self.sender_emails_tab = SenderEmailsTab(self.page.get_by_role('tabpanel'))
        self.emails_received_tab = EmailsReceivedTab(self.page.get_by_label('tabpanel'))
        self.add_email_domain_popup = AddEmailDomainPopup(
            self.page.get_by_role('dialog')
        )
        self.remove_email_domain_popup = RemoveEmailDomainPopup(
            self.page.get_by_role('dialog')
        )

    @allure.step('SenderDetailsPage: add to block list')
    def add_to_block_list(self, is_email: bool) -> str:
        self.add_to_block_list_button.click()
        email_domain = self.add_email_domain_popup.add_email_domain(is_email)
        self.add_email_domain_popup.block_button.click()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_blocked_list_success_message
        )
        return email_domain

    @allure.step('SenderDetailsPage: add to safe list')
    def add_to_safe_list(self, is_email: bool) -> str:
        self.add_to_safe_list_button.click()
        email_domain = self.add_email_domain_popup.add_email_domain(is_email)
        self.add_email_domain_popup.mark_as_safe_button.click()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_safe_list_success_message
        )
        return email_domain

    @allure.step('SenderDetailsPage: remove from list')
    def remove_from_list(self, list_name: str):
        match list_name:
            case 'Block List':
                self.unblock_button.click()
            case 'Safe List':
                self.remove_from_safe_list_button.click()
            case _:
                raise ValueError(f'List {list_name} is not supported')
        self.remove_email_domain_popup.confirm()

    @allure.step('SenderDetailsPage: get sender details')
    def get_sender_details(self):
        return {
            'sender_domain': self.sender_domain_text.text_content(),
            'first_contacted': self.first_contacted_text.text_content(),
            'last_received': self.last_received_text.text_content(),
            'no_of_emails_received': self.no_of_emails_received_text.text_content(),
            'no_of_employees_received': self.no_of_employees_received_text.text_content(),
            'highest_risk_level': self.highest_risk_level_text.text_content(),
            'average_risk_level': self.average_risk_level_text.text_content(),
            'blocked_safe_status': self.blocked_safe_status_text.text_content(),
        }


class SenderEmailsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_by_email = self.locator.get_by_role(
            'textbox', name='Search by email'
        )
        self.sender_emails_table = Table(
            self.locator.locator('.MuiDataGrid-row'), SenderEmailsTableComponent
        )


class SenderEmailsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.date_received = self.locator.locator('[data-field="received_time"]')
        self.subject = self.locator.locator('[data-field="subject"]')
        self.risk_level = self.locator.locator('[data-field="verdict"]')


class EmailsReceivedTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.search_by_email = self.locator.get_by_role(
            'textbox', name='Search by email'
        )
        self.emails_received_table = Table(
            self.locator.locator('.MuiDataGrid-row'), EmailsReceivedTableComponent
        )


class EmailsReceivedTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.name = self.locator.locator('[data-field="name"]')
        self.email_address = self.locator.locator('[data-field="email_address"]')


class AddEmailDomainPopup:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.email_address = self.locator.get_by_role('radio', name='Email Address')
        self.domain = self.locator.get_by_role('radio', name='Domain')
        self.input = self.locator.get_by_role('textbox')
        self.block_button = self.locator.get_by_role('button', name='Block')
        self.mark_as_safe_button = self.locator.get_by_role(
            'button', name='Mark As Safe'
        )

    def add_email_domain(self, is_email: bool):
        if is_email:
            self.email_address.click()
        else:
            self.domain.click()
        email_domain = self.input.get_attribute('value')
        return email_domain


class RemoveEmailDomainPopup:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.confirm_button = self.locator.get_by_role(
            'button', name='Unblock'
        ) or self.locator.get_by_role('button', name='Remove')
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')

    def confirm(self):
        self.confirm_button.click()
