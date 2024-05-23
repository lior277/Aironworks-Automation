import re
import allure
from typing import Literal
from playwright.sync_api import Page, expect
from src.utils.assertions import is_selected
from src.page_objects.base_page import BasePage
from src.models.auth.user_model import UserModel


class CustomersPage(BasePage):
    def __init__(self, page: Page, user: UserModel):
        super().__init__(page)
        self.user = user
        self.tabs = {
            "active": page.get_by_role("tab", name=re.compile("Active customers.*")),
            "new": page.get_by_role("tab", name=re.compile("New customers.*")),
            "past": page.get_by_role("tab", name=re.compile("Past customers.*")),
        }
        self.active_customers_table_headers = [
            page.get_by_role("columnheader", name=re.compile("Company.*")),
            page.get_by_role("columnheader", name=re.compile("Status.*")),
            page.get_by_role("columnheader", name=re.compile("Employee limit.*")),
            page.get_by_role("columnheader", name=re.compile("Actions.*")),
        ]
        self.copy_invitation_link_button = page.get_by_label(
            "Copy a unique link to invite"
        )
        if not user.is_reseller:
            self.active_customers_table_headers.append(
                page.get_by_role("columnheader", name=re.compile("Reseller.*")),
            )

    @allure.step("CustomersPage: validate everything is visible")
    def validate_elements_visible(self):
        for tab in self.tabs.values():
            expect(tab).to_be_visible()

    @allure.step("CustomersPage: validate tab is selected")
    def validate_in_tab(self, tab_name: Literal["active", "new", "past"]):
        is_selected(self.tabs[tab_name])

    @allure.step("CustomersPage: validate all active customers headers are visible")
    def validate_active_customers_headers_are_visible(self):
        for header in self.active_customers_table_headers:
            expect(header).to_be_visible()

    @allure.step
    def get_customer_row(self):
        return self.page.get_by_role("row").nth(1)
