import allure

from .base_page import BasePage
from .employee_table_component import EmployeeTableComponent


class ExecuteCampaignPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.pick_employees = page.get_by_role('button', name='+ Pick Employees')
        self.review_button = page.get_by_role('button', name='Review')
        self.execute_button = page.get_by_role('button', name='Execute')
        self.confirm_execute_button = page.get_by_role('button', name='Confirm')
        self.number_of_employees = page.get_by_text(
            'Number of targets in this campaign:'
        ).locator('span')
        self.employee_table = EmployeeTableComponent(page.get_by_test_id('table'), page)

    @allure.step('ExecuteCampaignPage: pick {company_name} company')
    def pick_company(self, company_name: str):
        self.page.get_by_label('Customer').click()
        self.page.get_by_role('option', name=company_name, exact=True).click()
        return self
