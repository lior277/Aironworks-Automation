import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.filter import Filter
from src.page_objects.data_types.table_element import Table


class CreateGroupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.create_button = self.page.get_by_role('button', name='Create')
        self.select_button = self.page.get_by_role('button', name='Select')
        self.add_managers_button = self.page.get_by_role('button', name='Add Managers')
        self.add_members_button = self.page.get_by_role('button', name='Add Members')
        self.name_input = self.page.locator('[name="name"]')
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
        self.filter_tooltip = self.page.get_by_role('tooltip').filter(
            has_text='Email contains'
        )

    @allure.step('CreateGroupPage: create {group_name} group')
    def create_group(
        self,
        group_name: str,
        managers_email: list[str] = None,
        employees_email: list[str] = None,
    ):
        self.name_input.fill(group_name)
        if managers_email:
            self.add_managers_button.click()
            for email in managers_email:
                self.filter.filter_by('Email', email)
                self.filter.button.hover()
                self.filter_tooltip.click()
                self.filter_tooltip.wait_for(state='hidden')
                manager = self.table_choose_employees.get_row_by_column_value(
                    'email', email
                )
                manager.checkbox.check()
            self.select_button.click()
            for email in managers_email:
                expect(
                    self.table_managers.get_row_by_column_value('email', email).email
                ).to_have_text(email)
        if employees_email:
            self.add_members_button.click()
            for email in employees_email:
                self.filter.filter_by('Email', email)
                self.filter.button.hover()
                self.filter_tooltip.click()
                self.filter_tooltip.wait_for(state='hidden')
                employee = self.table_choose_employees.get_row_by_column_value(
                    'email', email
                )
                employee.checkbox.check()
            self.select_button.click()
            for email in employees_email:
                expect(
                    self.table_employees.get_row_by_column_value('email', email).email
                ).to_have_text(email)
        self.create_button.click()


class ChooseEmployeesTableComponent:
    def __init__(self, locator: Locator):
        self.checkbox = locator.get_by_label('Select row')
        self.first_name = locator.locator('[data-field="first_name"]')
        self.last_name = locator.locator('[data-field="last_name"]')
        self.email = locator.locator('[data-field="email"]')
        self.language = locator.locator('[data-field="language"]')
        self.groups = locator.locator('[data-field="groups"]')


class ManagersTableComponent:
    def __init__(self, locator: Locator):
        self.email = locator.get_by_role('heading', level=6)
        self.full_name = locator.locator('/div/p')
        self.remove_button = locator.get_by_role('button')


class EmployeesTableComponent:
    def __init__(self, locator: Locator):
        self.checkbox = locator.get_by_label('Select row')
        self.email = locator.locator('[data-field="email"]')
        self.full_name = locator.locator('[data-field="full_name"]')
