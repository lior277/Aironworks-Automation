from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table


class CompletedEducationCampaignsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.dashboard_breadcrumbs = self.page.get_by_role('link', name='Dashboard')
        self.back_button = self.page.get_by_role('button', name='Back')
        self.completed_education_campaigns_table = Table(
            self.page.locator('//*[contains(@class,"MuiDataGrid-row")]'),
            CompletedEducationCampaignsTableComponent,
        )

    def get_first_row_data(self):
        self.completed_education_campaigns_table.wait_for_loading()
        row = self.completed_education_campaigns_table.get_row_by_index(0)
        if not row:
            raise Exception('No rows found in the table')
        return row.to_dict()

    def click_first_row(self):
        self.completed_education_campaigns_table.wait_for_loading()
        row = self.completed_education_campaigns_table.get_row_by_index(0)
        if not row:
            raise Exception('No rows found in the table')
        row.title.click()


class CompletedEducationCampaignsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('[data-field="campaign.title"]')
        self.completed_date = self.locator.locator('[data-field="date_submitted"]')
        self.quiz_score = self.locator.locator('[data-field="score"]')

    def to_dict(self):
        return {
            'title': self.title.text_content(),
            'completed_date': self.completed_date.text_content(),
            'quiz_score': self.quiz_score.text_content(),
        }
