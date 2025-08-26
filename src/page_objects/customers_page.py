import re
from typing import Literal

import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.utils.assertions import is_selected


class CustomersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = self.page.get_by_role('heading', level=2, name='Customers')
        self.tabs = {
            'active': page.get_by_role('tab', name=re.compile('Active customers.*')),
            'new': page.get_by_role('tab', name=re.compile('New customers.*')),
            'past': page.get_by_role('tab', name=re.compile('Past customers.*')),
        }
        self.active_customers_table_headers = page.get_by_role('columnheader')
        self.copy_invitation_link_button = page.get_by_label(
            'Copy a unique link to invite'
        )
        self.new_customers_table = Table(
            page.locator('//button[text()="Approve"]//ancestor::div[@role="row"]'),
            NewCustomer,
        )
        self.confirm_approval_button = page.get_by_role(
            'button', name='Confirm Approval'
        )

    @allure.step('CustomersPage: validate everything is visible')
    def validate_elements_visible(self):
        for tab in self.tabs.values():
            expect(tab).to_be_visible()

    @allure.step('CustomersPage: validate tab is selected')
    def validate_in_tab(self, tab_name: Literal['active', 'new', 'past']):
        is_selected(self.tabs[tab_name])

    @allure.step('CustomersPage: validate all active customers headers are visible')
    def validate_active_customers_headers_are_visible(self):
        for header in self.active_customers_table_headers.all():
            expect(header).to_be_visible()

    @allure.step
    def get_customer_row(self):
        return self.page.get_by_role('row').nth(1)

    def navigate_to_new_customers_page(self):
        self.tabs['new'].click()

    def approve_customer(self, company_name: str):
        self.new_customers_table.get_row_by_column_value(
            'company', company_name
        ).approve()
        self.confirm_approval_button.click()
        self.ensure_alert_message_is_visible('Company successfully approved.')


class NewCustomer:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.company = self.locator.locator('[data-field="company_name"]')
        self.reseller = self.locator.locator('[data-field="reseller_company_name"]')
        self.admin_email = self.locator.locator('[data-field="email"]')
        self.admin_first_name = self.locator.locator('[data-field="first_name"]')
        self.admin_last_name = self.locator.locator('[data-field="last_name"]')
        self.registration_date = self.locator.locator('[data-field="time_created"]')
        self.reject_button = self.locator.get_by_role('button', name='Reject')
        self.approve_button = self.locator.get_by_role('button', name='Approve')

    def reject(self):
        self.reject_button.click()

    def approve(self):
        self.approve_button.click()
