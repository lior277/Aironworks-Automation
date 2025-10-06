import allure

from src.page_objects.data_types.filter import Filter

from .base_page import BasePage
from .employee_table_component import EmployeeTableComponent
from .warning_page import WarningPage


class ExecuteCampaignPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pick_employees = page.get_by_role('button', name='+ Pick Employees')
        self.review_button = page.get_by_role('button', name='Review')
        self.execute_button = page.get_by_role('button', name='Execute')
        self.confirm_execute_button = page.get_by_role('button', name='Confirm')
        self.execution_date = page.get_by_role('textbox', name='Execution date')
        self.completion_date = page.get_by_role('textbox', name='Completion date')
        self.number_of_employees = page.get_by_text(
            'Number of targets in this campaign:'
        ).locator('span')
        self.employee_table = EmployeeTableComponent(page.get_by_test_id('table'), page)
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.get_by_role('combobox', name='Columns'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
            self.page.get_by_role('presentation'),
        )

        self.scheduled_text = page.get_by_role('alert').locator(
            'div[contains(., "You are about to execute a scheduled attack on:")]'
        )

    @allure.step('ExecuteCampaignPage: pick {company_name} company')
    def pick_company(self, company_name: str):
        self.page.get_by_label('Customer').click()
        self.page.get_by_role('option', name=company_name, exact=True).click()
        return self

    @allure.step(
        'ExecuteCampaignPage: select execution time {execution_time} and completion time {completion_time}'
    )
    def select_time(self, execution_time: str, completion_time=None):
        self.execution_date.fill(execution_time)
        if completion_time:
            self.completion_date.fill(completion_time)
        return self

    @allure.step('ExecuteCampaignPage: go to employeee campaign warnign page')
    def go_to_employee_campaign_warning_page(self, url: str):
        self.page.goto(url)
        return WarningPage(self.page)
