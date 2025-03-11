import tempfile
import time

import allure
from playwright.sync_api import Locator, Page, expect

from src.models.company.employee_list_model import EmployeeItemModel
from src.page_objects.base_page import BasePage
from src.page_objects.const import (
    file_type_must_be_csv_xlsx,
    get_file_size_error_message,
)
from src.page_objects.data_types.filter import Filter
from src.page_objects.data_types.table_element import Table
from src.page_objects.employee_directory.add_admin_page import AddAdminPage
from src.page_objects.employee_directory.const import (
    deactivated_employees_success_message,
    employees_deleted_message,
    employees_restored_message,
)
from src.page_objects.employee_directory.edit_employee_page import EditEmployeePage
from src.page_objects.entity.employee_entity import (
    EmployeeEntity,
    EmployeeEntityFactory,
)
from src.utils.log import Log


class EmployeeDirectoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.get_by_role(
            'heading', level=2, name='Employee Directory'
        )
        self.company_employees_tab = self.page.get_by_role(
            'tab', name='Company Employees'
        )
        # contain name
        self.admins_tab = self.page.locator(
            '//button[@role="tab" and contains(@id,"/admins")]'
        )
        self.inactive_tab = self.page.get_by_role('tab', name='Inactive')
        self.upload_employees_button = self.page.get_by_role(
            'button', name='Upload Employees', exact=True
        )
        self.add_admin_button = self.page.get_by_role('button', name='Add Admin')
        self.upload_csv_button = self.page.get_by_label('Upload a CSV')
        self.upload_azure_ad_button = self.page.get_by_label('Upload via Azure AD')
        self.export_csv_button = self.page.get_by_role('button', name='Export CSV')
        self.deactivate_button = self.page.get_by_role('button', name='Deactivate')
        self.edit_button = self.page.get_by_label('Edit')
        self.restore_button = self.page.get_by_role('button', name='Restore')
        self.delete_button = self.page.get_by_role('button', name='Delete')
        self.show_filters_button = self.page.get_by_label('Show filters')
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.locator('select', has_text='Email'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
        )

        self.add_new_employees_only_button = self.page.get_by_role(
            'button', name='Add new employees only'
        )
        self.overwrite_existing_button = self.page.get_by_role(
            'button', name='Overwrite existing'
        )
        self.select_total_checkbox = self.page.get_by_role('button', name='Deactivate')
        self.upload_employees_component = UploadEmployeesComponent(
            self.page.get_by_role(role='dialog')
        )
        self.deactivate_employees_component = DeactivateEmployeesComponent(
            self.page.get_by_role(role='dialog', name='Deactivate Employees')
        )
        self.delete_employees_component = DeleteEmployeesComponent(
            self.page.get_by_role(role='dialog', name='Delete Employees')
        )

        self.rejected_upload_component = RejectedUploadItemComponent(
            self.page.get_by_label('rejected-upload-item')
        )
        self.table_employees = Table(
            page.locator('[aria-label="Employee row"]'), EmployeesTableComponent
        )
        self.table_inactive = Table(
            self.page.locator('.MuiDataGrid-row'), EmployeesTableComponent
        )
        self.employee_checkbox = page.locator(
            '[type="checkbox"][aria-label="Select row"]'
        )

    @allure.step('EmployeeDirectoryPage: upload file {file_path} override = {override}')
    def upload_file(self, file_path: str, override: bool = False):
        if self.upload_employees_button.is_visible():
            self.upload_employees_button.click()
        if self.upload_csv_button.is_visible():
            self.upload_csv_button.click()
        expect(self.upload_employees_component.locator).to_be_visible()
        with self.page.expect_file_chooser() as fc:
            self.upload_employees_component.upload_button.click()
            fc.value.set_files(file_path)
            if self.rejected_upload_component.locator.is_visible():
                expect(self.rejected_upload_component.description).to_have_text(
                    file_type_must_be_csv_xlsx
                )
                expect(self.rejected_upload_component.header).to_contain_text(
                    get_file_size_error_message(file_path)
                )
            else:
                if override:
                    self.overwrite_existing_button.click()
                else:
                    self.add_new_employees_only_button.click()
                expect(self.loading).to_be_visible()
                expect(self.upload_employees_component.locator).not_to_be_visible(
                    timeout=30000
                )

    @allure.step('EmployeeDirectoryPage: download csv file')
    def download_csv_file(self, with_additional_fields: bool = False):
        self.upload_employees_button.click()
        self.upload_csv_button.click()
        expect(self.upload_employees_component.locator).to_be_visible()
        path = tempfile.mktemp(suffix='.csv')
        with self.page.expect_download() as download_info:
            if with_additional_fields:
                self.upload_employees_component.download_optional_button.click()
            else:
                self.upload_employees_component.download_required_button.click()
        download_event = download_info.value
        download_event.save_as(path)
        Log.info(f'{path=}')
        self.page.keyboard.press('Escape')
        time.sleep(1)
        return path

    @allure.step('EmployeeDirectoryPage: filter employee by {email} email')
    def filter_employee_by_email(self, email: str):
        self.filter.filter_by('Email', email)
        self.wait_for_loading_state()
        self.title.hover()

    @allure.step('EmployeeDirectoryPage: edit employee to {expected_employee} values')
    def edit_employee(self, expected_employee: EmployeeItemModel):
        self.edit_button.click()
        self.wait_for_progress_bar_disappears()
        edit_employee_page = EditEmployeePage(self.page)
        edit_employee_page.edit_employee(expected_employee)

    @allure.step('EmployeeDirectoryPage: get employee entity by {email} email')
    def get_employee_entity_by_email(self, email: str) -> EmployeeEntity:
        self.filter_employee_by_email(email)
        out = self.table_employees.text_content()
        return EmployeeEntityFactory.get_entity_from_dict(out[0])

    @allure.step('EmployeeDirectoryPage: deactivate employee by {email} email')
    def deactivate_employee(self, email: str):
        self.filter_employee_by_email(email)
        self.employee_checkbox.check()
        self.deactivate_button.click()
        self.deactivate_employees_component.ok_button.click()
        self.ensure_alert_message_is_visible(deactivated_employees_success_message)

    @allure.step('EmployeeDirectoryPage: restore employee by {email} email')
    def restore_employee(self, email: str):
        self.inactive_tab.click()
        self.filter_employee_by_email(email)
        self.employee_checkbox.check()
        self.restore_button.click()
        self.ensure_alert_message_is_visible(employees_restored_message)

    @allure.step('EmployeeDirectoryPage: delete employee by {email} email')
    def delete_employee(self, email: str):
        self.inactive_tab.click()
        self.delete_button.wait_for()
        self.wait_for_loading_state()
        self.filter_employee_by_email(email)
        self.employee_checkbox.check()
        self.delete_button.click()
        self.delete_employees_component.ok_button.click()
        self.ensure_alert_message_is_visible(employees_deleted_message)

    @allure.step('EmployeeDirectoryPage: go to add admin page')
    def go_to_add_admin_page(self):
        self.admins_tab.click()
        self.add_admin_button.click()
        add_admin_page = AddAdminPage(self.page)
        add_admin_page.wait_for_loading_state()
        return add_admin_page


class EmployeesTableComponent:
    def __init__(self, locator: Locator):
        self.first_name = locator.locator('[data-field="first_name"]')
        self.last_name = locator.locator('[data-field="last_name"]')
        self.email = locator.locator('[data-field="email"]')
        self.language = locator.locator('[data-field="language"]')
        self.linked_in = locator.locator('[data-field="linkedin"]')
        self.twitter = locator.locator('[data-field="twitter"]')
        self.dial_code = locator.locator('[data-field="dial_code"]')
        self.instagram = locator.locator('[data-field="instagram"]')
        self.mobile_number = locator.locator('[data-field="national_number"]')
        self.facebook = locator.locator('[data-field="facebook"]')


class UploadEmployeesComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.upload_button = self.locator.get_by_text(
            'Or Select A File From Your Computer'
        )
        self.download_required_button = self.locator.get_by_text(
            'Download Required Fields CSV'
        )
        self.download_optional_button = self.locator.get_by_text(
            'Download Required and Optional Fields CSV'
        )


class RejectedUploadItemComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.header = self.locator.get_by_role('heading', level=6)
        self.description = self.locator.locator('//div/p')


class DeactivateEmployeesComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.ok_button = self.locator.get_by_role('button', name='OK')
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')


class DeleteEmployeesComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.ok_button = self.locator.get_by_role('button', name='OK')
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')
        self.description = self.locator.locator('//div/p')
