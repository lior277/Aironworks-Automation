import allure
from playwright.sync_api import Locator, Page, expect

from src.models.email_filter.email_domain_model import EmailDomainModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.email_filter.const import (
    TabName,
    add_email_domain_to_blocked_list_success_message,
    add_email_domain_to_safe_list_success_message,
    block_high_risk_emails_success_message,
    label_as_high_risk_only_success_message,
    remove_email_domain_from_blocked_list_success_message,
    remove_email_domain_from_safe_list_success_message,
)


class EmailFilterSettingsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.blocked_list = self.page.get_by_role('tab', name='Blocked List')
        self.safe_list = self.page.get_by_role('tab', name='Safe List')
        self.high_risk_emails = self.page.get_by_role('tab', name='High Risk Emails')

        self.blocked_list_tab = BlockedListTab(
            self.page.get_by_label('EmailBlockedListTab')
        )
        self.safe_list_tab = SafeListTab(self.page.get_by_label('SafeListTab'))
        self.high_risk_emails_tab = HighRiskEmailsTab(
            self.page.get_by_label('HighRiskEmailsTab')
        )
        self.add_email_domain_popup = AddEmailDomainPopup(
            self.page.get_by_role('dialog')
        )
        self.remove_email_domain_popup = RemoveEmailDomainPopup(
            self.page.get_by_role('dialog')
        )

    @allure.step('EmailFilterSettingsPage: open tab {tab_name}')
    def open_tab(self, tab_name: str):
        match tab_name:
            case TabName.BLOCKED_LIST:
                self.blocked_list.click()
                self.blocked_list_tab.block_list_table.wait_for_loading()
            case TabName.SAFE_LIST:
                self.safe_list.click()
                self.safe_list_tab.safe_list_table.wait_for_loading()
            case TabName.HIGH_RISK_EMAIL_SETTINGS:
                self.high_risk_emails.click()
            case _:
                raise ValueError(f'Tab {tab_name} is not supported')

    def add_to_block_list(self, email_domain: EmailDomainModel):
        self.blocked_list_tab.add_to_block_list_button.click()
        expect(self.add_email_domain_popup.locator).to_be_visible()
        self.add_email_domain_popup.add_email_domain(email_domain)
        self.add_email_domain_popup.block_button.click()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_blocked_list_success_message
        )

    def add_to_safe_list(self, email_domain: EmailDomainModel):
        self.open_tab('Safe List')
        self.safe_list_tab.add_to_safe_list_button.click()
        expect(self.add_email_domain_popup.locator).to_be_visible()
        self.add_email_domain_popup.add_email_domain(email_domain)
        self.add_email_domain_popup.mark_as_safe_button.click()
        self.ensure_alert_message_is_visible(
            add_email_domain_to_safe_list_success_message
        )

    @allure.step('EmailFilterSettingsPage: remove last data from block list')
    def remove_from_block_list(self):
        self.blocked_list_tab.block_list_table.get_last_row().actions.click()
        expect(self.remove_email_domain_popup.locator).to_be_visible()
        self.remove_email_domain_popup.unblock_button.click()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_blocked_list_success_message
        )

    @allure.step('EmailFilterSettingsPage: remove last data from safe list')
    def remove_from_safe_list(self):
        self.open_tab('Safe List')
        self.safe_list_tab.safe_list_table.get_last_row().actions.click()
        expect(self.remove_email_domain_popup.locator).to_be_visible()
        self.remove_email_domain_popup.remove_button.click()
        self.ensure_alert_message_is_visible(
            remove_email_domain_from_safe_list_success_message
        )

    @allure.step(
        'EmailFilterSettingsPage: update high risk emails handling option to {option}'
    )
    def update_high_risk_emails_handling(self, option: str):
        self.open_tab('High Risk Emails')
        match option:
            case 'Block High-Risk Email':
                self.high_risk_emails_tab.block_high_risk_emails()
                self.ensure_alert_message_is_visible(
                    block_high_risk_emails_success_message
                )
            case 'Label As High-Risk Only':
                self.high_risk_emails_tab.label_as_high_risk_only()
                self.ensure_alert_message_is_visible(
                    label_as_high_risk_only_success_message
                )
            case _:
                raise ValueError(f'Option {option} is not supported')


class BlockedListTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.add_to_block_list_button = self.locator.get_by_role(
            'button', name='Add to block list'
        )
        self.block_list_table = Table(
            self.locator.locator('.MuiDataGrid-row'), ListTableComponent
        )


class SafeListTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.add_to_safe_list_button = self.locator.get_by_role(
            'button', name='Add to safe list'
        )
        self.safe_list_table = Table(
            self.locator.locator('.MuiDataGrid-row'), ListTableComponent
        )


class ListTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.email_domain = self.locator.locator('[data-field="link"]')
        self.actions = self.locator.locator('[data-field="actions"]').locator('button')


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
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')

    def add_email_domain(self, email_domain: EmailDomainModel):
        if email_domain.email_address:
            self.email_address.click()
            self.input.fill(email_domain.email_address)
        elif email_domain.domain:
            self.domain.click()
            self.input.fill(email_domain.domain)


class RemoveEmailDomainPopup:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.unblock_button = self.locator.get_by_role('button', name='Unblock')
        self.remove_button = self.locator.get_by_role('button', name='Remove')
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')


class HighRiskEmailsTab:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.block_high_risk_emails_option = self.locator.get_by_label(
            'Block high-risk email'
        )
        self.label_as_high_risk_only_option = self.locator.get_by_label(
            'Label as high-risk only'
        )
        self.save_button = self.locator.get_by_role('button', name='Save')
        self.discard_button = self.locator.get_by_role('button', name='Discard')

    def block_high_risk_emails(self):
        self.block_high_risk_emails_option.click()
        expect(self.save_button).to_be_visible()
        self.save_button.click()

    def label_as_high_risk_only(self):
        self.label_as_high_risk_only_option.click()
        expect(self.save_button).to_be_visible()
        self.save_button.click()
