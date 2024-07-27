import allure
import time
from playwright.sync_api import Locator, Page, expect


class EmployeeRow:
    def __init__(self, locator: Locator):
        self.locator = locator

    def select_row(self):
        self.locator.get_by_label('Select row').click()


class EmployeeTableComponent:
    def __init__(self, component: Locator, page: Page) -> None:
        self.table = component
        self.page = page
        self.filters_button = self.table.get_by_label('Show filters')
        self.filter_column = self.page.get_by_label('Columns')
        self.filter_value = self.page.get_by_placeholder('Filter value')

    @allure.step('EmployeeTableComponent: set filter column')
    def set_filter_column(self, column: str, value: str, nth: int = 0) -> None:
        self.filters_button.click()
        times = 0
        while times < 10:
            self.filter_column.nth(nth).select_option(column)
            self.filter_value.fill(value)
            try:
                expect(self.filter_column).to_have_value(column)
                break
            except AssertionError:
                times += 1
                time.sleep(1)
        self.page.wait_for_load_state(timeout=5)
        expect(self.table.get_by_test_id('empty-state')).to_have_count(0)
        time.sleep(1)  # TODO: find another way to wait for the filters UI to disappear
        single_row = self.table.get_by_role('row').first
        expect(single_row).to_be_visible()
        single_row.click()
        time.sleep(1)

    @allure.step('EmployeeTableComponent: get employee row')
    def get_employee_row(self, email: str) -> EmployeeRow:
        return EmployeeRow(self.table.get_by_role('row').filter(has_text=email).first)
