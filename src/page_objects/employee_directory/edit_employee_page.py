import allure
from playwright.sync_api import Page

from src.models.company.employee_list_model import EmployeeItemModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown


class EditEmployeePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name = self.page.locator('[id="firstName"]')
        self.last_name = self.page.locator('[id="lastName"]')
        self.email = self.page.locator('[id="email"]')
        self.language = DropDown(
            link_locator=self.page.locator('[aria-labelledby="language-label"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.dial_code = self.page.locator('[id="dialCode"]')
        self.mobile_number = self.page.locator('[id="nationalNumber"]')
        self.facebook = self.page.locator('[id="facebook"]')
        self.twitter = self.page.locator('[id="twitter"]')
        self.linked_in = self.page.locator('[id="linkedIn"]')
        self.instagram = self.page.locator('[id="instagram"]')
        self.save_changes_button = self.page.get_by_role('button', name='Save Changes')
        self.cancel_button = self.page.get_by_role('button', name='Cancel')

    @allure.step('EditEmployeePage: edit employee to {expected_employee} values')
    def edit_employee(self, expected_employee: EmployeeItemModel):
        if expected_employee.first_name:
            self.first_name.fill(expected_employee.first_name)
        if expected_employee.last_name:
            self.last_name.fill(expected_employee.last_name)
        if expected_employee.email:
            self.email.fill(expected_employee.email)
        if expected_employee.language:
            self.language.select_item_by_text(expected_employee.language)
        if expected_employee.attack_vector_addresses:
            for attack in expected_employee.attack_vector_addresses:
                if attack.attack_vector == 'dial_code':
                    self.dial_code.fill(attack.value)
                if attack.attack_vector == 'national_number':
                    self.mobile_number.fill(attack.value)
                if attack.attack_vector == 'facebook':
                    self.facebook.fill(attack.value)
                if attack.attack_vector == 'twitter':
                    self.twitter.fill(attack.value)
                if attack.attack_vector == 'linkedin':
                    self.linked_in.fill(attack.value)
                if attack.attack_vector == 'instagram':
                    self.instagram.fill(attack.value)
        self.save_changes_button.click()
