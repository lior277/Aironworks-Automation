import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects import (
    file_type_must_be_csv_xlsx,
    get_file_size_error_message,
    update_succeeded_text,
)
from src.page_objects.base_page import BasePage


class EmployeeDirectoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.company_employees_tab = self.page.get_by_role(
            'tab', name='Company Employees'
        )
        self.admins_tab = self.page.get_by_role('tab', name='Admins')
        self.inactive_tab = self.page.get_by_role('tab', name='Inactive')
        self.upload_employees_button = self.page.get_by_role(
            'button', name='Upload Employees'
        )
        self.export_csv_button = self.page.get_by_role('button', name='Export CSV')
        self.deactivate_button = self.page.get_by_role('button', name='Deactivate')
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

    @allure.step('EmployeeDirectoryPage: upload file {file_path} override = {override}')
    def upload_file(self, file_path: str, override: bool = False):
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
                expect(self.alert_message).to_contain_text(update_succeeded_text)


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
