import tempfile

import allure
from playwright.sync_api import Locator, Page, expect

from src.models.company.employee_list_model import EmployeeItemModel
from src.page_objects import file_type_must_be_csv_xlsx, get_file_size_error_message
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.filter import Filter
from src.page_objects.data_types.table_element import Table
from src.page_objects.employee_directory.edit_employee_page import EditEmployeePage
from src.page_objects.entity.employee_entity import (
    EmployeeEntity,
    EmployeeEntityFactory,
)
from src.utils.log import Log


class EmployeeDirectoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.company_employees_tab = self.page.get_by_role(
            'tab', name='Company Employees'
        )
        self.admins_tab = self.page.get_by_role('tab', name='Admins')
        self.inactive_tab = self.page.get_by_role('tab', name='Inactive')
        self.upload_employees_button = self.page.get_by_role(
            'button', name='Upload Employees', exact=True
        )
        self.export_csv_button = self.page.get_by_role('button', name='Export CSV')
        self.deactivate_button = self.page.get_by_role('button', name='Deactivate')
        self.edit_button = self.page.get_by_label('Edit')
        self.show_filters_button = self.page.get_by_label('Show filters')
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.locator('select', has_text='Email'),
            self.page.locator('[placeholder="Filter value"]'),
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
        self.rejected_upload_component = RejectedUploadItemComponent(
            self.page.get_by_label('rejected-upload-item')
        )
        self.table_employees = Table(
            page.locator('[aria-label="Employee row"]'), EmployeesTableComponent
        )

    @allure.step('EmployeeDirectoryPage: upload file {file_path} override = {override}')
    def upload_file(self, file_path: str, override: bool = False):
        if self.upload_employees_button.is_visible():
            self.upload_employees_button.click()
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
                self.wait_for_loading_state()
                expect(self.upload_employees_component.locator).not_to_be_visible()

    @allure.step('EmployeeDirectoryPage: download csv file')
    def download_csv_file(self, with_additional_fields: bool = False):
        self.upload_employees_button.click()
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
        return path

    @allure.step('EmployeeDirectoryPage: filter employee by {email} email')
    def filter_employee_by_email(self, email: str):
        self.filter.filter_by('Email', email)
        assert (
            len(self.table_employees.get_content()) == 1
        ), f'{self.table_employees.get_content()=}'

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
        assert len(out) == 1
        return EmployeeEntityFactory.get_entity_from_dict(out[0])


class EmployeesTableComponent:
    def __init__(self, locator: Locator):
        self.first_name = locator.locator('[data-field="first_name"]')
        self.last_name = locator.locator('[data-field="last_name"]')
        self.email = locator.locator('[data-field="email"]')
        self.language = locator.locator('[data-field="language"]')
        self.mobile_number = locator.locator('[data-field="national_number"]')
        self.linked_in = locator.locator('[data-field="linkedin"]')
        self.instagram = locator.locator('[data-field="instagram"]')
        self.dial_code = locator.locator('[data-field="dial_code"]')
        self.facebook = locator.locator('[data-field="facebook"]')
        self.twitter = locator.locator('[data-field="twitter"]')


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
