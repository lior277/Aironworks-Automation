import allure
from playwright.sync_api import Page, expect

from src.models.company.employee_model import EmployeeModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.employee_directory.const import (
    add_admin_existing_employee_success_message,
    add_admin_success_message,
)


class AddAdminPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.breadcrumb = self.page.get_by_role('current-breadcrumb')
        self.alert_message = self.page.locator("[id='notistack-snackbar']")

        # Select option step
        self.create_new_admin_account_option = self.page.get_by_role(
            'radio', name='Create a New Admin Account'
        )
        self.assign_admin_role_option = self.page.get_by_role(
            'radio', name='Assign an Admin Role to the Employee'
        )
        self.cancel_button = self.page.get_by_role('button', name='Cancel')
        self.next_button = self.page.get_by_role('button', name='Next')

        # Add a New Admin step
        self.first_name = self.page.get_by_role('textbox', name='First Name')
        self.last_name = self.page.get_by_role('textbox', name='Last Name')
        self.email = self.page.get_by_role('textbox', name='Email')
        self.language_dropdown = DropDown(
            link_locator=self.page.locator('[aria-labelledby="language-label"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.add_admin_button = self.page.get_by_role(
            'button', name='Add New Admin & Send Invitation'
        )

        # Assign Admin Role step
        self.search_by_email = self.page.get_by_role(
            'searchbox', name='Search by Email'
        )
        self.select_all_rows = self.page.get_by_role('checkbox', name='Select all rows')
        self.rows_checkbox = self.page.get_by_role('checkbox', name='Select row')
        self.first_name_sort = self.page.locator('div[text()="First Name"]')
        self.last_name_sort = self.page.locator('div[text()="Last Name"]')
        self.email_sort = self.page.locator('div[text()="Email"]')
        self.language_sort = self.page.locator('div[text()="Language"]')
        self.aw_group_sort = self.page.locator('div[text()="AW Group"]')
        self.next_page_button = self.page.get_by_role('button', name='Go to next page')
        self.previous_page_button = self.page.get_by_role(
            'button', name='Go to previous page'
        )
        self.confirm_button = self.page.get_by_role(
            'button', name='Confirm & Assign An Admin Role'
        )

    @allure.step('AddAdminPage: select assign new employee {create_new} from list')
    def select_option(self, create_new: bool):
        if create_new:
            self.create_new_admin_account_option.click()
        else:
            self.assign_admin_role_option.click()
        self.next_button.click()

    @allure.step('AddAdminPage: add new admin {employee} and send invitation')
    def add_new_admin(self, employee: EmployeeModel):
        self.first_name.fill(employee.first_name)
        self.last_name.fill(employee.last_name)
        self.email.fill(employee.email)
        self.language_dropdown.select_item_by_text(employee.language)
        self.add_admin_button.click()

    @allure.step('AddAdminPage: assign admin role to employee with email {email}')
    def assign_admin_role(self, email: str):
        self.search_by_email.fill(email)
        self.rows_checkbox.nth(0).click()
        self.confirm_button.click()
        self.wait_for_progress_bar_disappears()
        expect(self.alert_message).to_contain_text(
            add_admin_existing_employee_success_message
        )

    @allure.step('AddAdminPage: add new admin {employee} and check invitation')
    def add_new_admin_and_check_invitation(self, employee: EmployeeModel):
        self.add_new_admin(employee)
        self.wait_for_progress_bar_disappears()
        expect(self.alert_message).to_contain_text(add_admin_success_message)

    @allure.step('AddAdminPage: add admin')
    def add_admin(self, employee: EmployeeModel, create_new: bool):
        self.select_option(create_new)
        if create_new:
            self.add_new_admin_and_check_invitation(employee)
        else:
            self.assign_admin_role(employee.email)
