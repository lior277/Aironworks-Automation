import tempfile

import allure
from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.filter import Filter
from src.page_objects.data_types.table_element import Table
from src.page_objects.groups.const import group_modified_successfully_text
from src.page_objects.groups.create_group_page import (
    ChooseEmployeesTableComponent,
    EmployeesTableComponent,
    ManagersTableComponent,
)
from src.page_objects.groups.group_details_page import GroupDetailsPage


class EditGroupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back', exact=True)
        self.save_button = self.page.get_by_role('button', name='Save')
        self.select_button = self.page.get_by_role('button', name='Select')
        self.name_input = self.page.locator('[name="name"]')
        self.add_managers_button = self.page.get_by_role('button', name='Add Managers')
        self.add_members_button = self.page.get_by_role('button', name='Add Members')
        self.remove_button = self.page.get_by_role('button', name='Remove')
        self.select_all_employees_checkbox = self.page.get_by_label('Select all rows')
        self.table_choose_employees = Table(
            page.locator('[role="row"].MuiDataGrid-row'), ChooseEmployeesTableComponent
        )

        self.table_managers = Table(
            page.locator('//*[@data-testid="PersonIcon"]/..'), ManagersTableComponent
        )
        self.table_employees = Table(
            page.locator('[role="row"].MuiDataGrid-row'), EmployeesTableComponent
        )

        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.locator('select', has_text='Email'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
        )
        self.export_button = self.page.get_by_role('button', name='Export CSV')

    @allure.step('EditGroupPage: edit group')
    def edit_group(
        self, group_name: str, remove_managers: bool, remove_employees: bool
    ):
        self.name_input.fill(group_name)
        if remove_managers:
            self.remove_all_managers()
        if remove_employees:
            self.remove_all_employees()
        self.save_button.click()
        self.ensure_alert_message_is_visible(
            group_modified_successfully_text, timeout=20000
        )
        return GroupDetailsPage(self.page)

    @allure.step('EditGroupPage: edit group {group_name} name')
    def edit_group_name(self, group_name):
        self.name_input.fill(group_name)

    @allure.step('EditGroupPage: remove all managers')
    def remove_all_managers(self):
        for manager in self.table_managers.get_content():
            manager.remove_button.click()
        expect(self.page.get_by_text('This group has no managers')).to_be_visible()

    @allure.step('EditGroupPage: remove all employees')
    def remove_all_employees(self):
        self.select_all_employees_checkbox.check()
        self.remove_button.click()
        expect(self.page.get_by_text('This group is empty')).to_be_visible()

    @allure.step('EditGroupPage: export employees as csv')
    def export_as_csv(self):
        path = tempfile.mktemp(suffix='.csv')
        with self.page.expect_download() as download_info:
            self.export_button.click()
        download_event = download_info.value
        download_event.save_as(path)
        return path
