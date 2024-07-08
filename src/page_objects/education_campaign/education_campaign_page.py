import allure
from playwright.sync_api import Page, Locator

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.education_campaign.education_campaign_details_page import EducationCampaignDetailsPage
from src.page_objects.entity.education_campaign_entity import EducationCampaignEntity


class EducationCampaignPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.table = Table(page.locator('//div[contains(@class,"MuiDataGrid-row")]'), EducationCampaignsTableComponent)

    @allure.step("EducationCampaignPage: education campaigns")
    def get_education_campaigns(self) -> list[EducationCampaignEntity]:
        out = []
        for row in self.table.get_content():
            out.append(EducationCampaignEntity(title=row.title.text_content(),
                                               assignments_submission_rate=row.assignments_submission_rate.text_content(),
                                               start_date=row.start_date.text_content(),
                                               end_date=row.end_date.text_content(),
                                               assignments_count=int(row.assignments_count.text_content()),
                                               company_name=row.company_name.text_content() if row.company_name.is_visible() else None))
        return out

    @allure.step("EducationCampaignPage: get education campaigns by {title} title")
    def get_education_campaign(self, title: str) -> EducationCampaignEntity:
        for campaign in self.get_education_campaigns():
            if campaign.title == title:
                return campaign

    @allure.step("EducationCampaignPage: open detail page for {title} education campaign")
    def open_campaign_details(self, title: str):
        row = self.table.get_row_by_column_value("title", title)
        row.title.click()
        details_page = EducationCampaignDetailsPage(self.page)
        details_page.title_txt.wait_for(timeout=5000, state="visible")
        return details_page


class EducationCampaignsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('[data-field="title"]')
        self.assignments_submission_rate = self.locator.locator('[data-field="assignments_submission_rate"]')
        self.start_date = self.locator.locator('[data-field="start_date"]')
        self.end_date = self.locator.locator('[data-field="end_date"]')
        self.assignments_count = self.locator.locator('[data-field="assignments_count"]')
        self.company_name = self.locator.locator('[data-field="company.name"]')
