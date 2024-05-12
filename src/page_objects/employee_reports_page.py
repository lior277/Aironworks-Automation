import re
from playwright.sync_api import Page
from src.page_objects.base_page import BasePage


class EmployeeReportsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.last_report_column_header = self.page.get_by_role(
            "columnheader", name=re.compile("Last Report.*")
        )

    def get_report(self, pattern):
        return self.page.get_by_role("row", name=pattern)
