import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.create_campaign_page import CreateCampaignPage
from src.page_objects.data_types.table_element import Table
from src.page_objects.education_campaign.education_campaign_details_page import (
    EducationCampaignDetailsPage,
)
from src.page_objects.entity.education_campaign_entity import EducationCampaignEntity


class EducationCampaignPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = page.get_by_role(
            'heading', level=4, name='Education Campaigns'
        ).nth(1)
        self.table = Table(
            page.get_by_role('rowgroup').locator(
                '//div[contains(@class,"MuiDataGrid-row")]'
            ),
            EducationCampaignsTableComponent,
        )
        self.create_education_campaign_button = self.page.get_by_role(
            'button', name='Create Education Campaign'
        )

    @allure.step('EducationCampaignPage: education campaigns')
    def get_education_campaigns(self) -> list[EducationCampaignEntity]:
        self.table.wait_for_loading(timeout=5000)
        out = []
        for row in self.table.get_content():
            out.append(row.to_entity())
            print('campaign:', row.to_entity())
        return out

    @allure.step('EducationCampaignPage: get education campaigns by {title} title')
    def get_education_campaign(self, title: str) -> EducationCampaignEntity:
        result = None
        for campaign in self.get_education_campaigns():
            if campaign.title == title:
                result = campaign
                break
        if not result:
            raise ValueError(f'Unable to find campaign by {title} title')
        return result

    @allure.step(
        'EducationCampaignPage: open detail page for {title} education campaign'
    )
    def open_campaign_details(self, title: str):
        row = self.table.get_row_by_column_value('title', title)
        if not row:
            raise ValueError(f'unable to find education campaign by {title} title')
        row.assignments_submission_rate.click()
        details_page = EducationCampaignDetailsPage(self.page)
        details_page.title_txt.wait_for(timeout=5000, state='visible')
        return details_page

    @allure.step('EducationCampaignPage: open create education campaign page')
    def open_create_campaign_page(self):
        self.create_education_campaign_button.click()
        return CreateCampaignPage(self.page)


class EducationCampaignsTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('[data-field="title"]')
        self.assignments_submission_rate = self.locator.locator(
            '[data-field="assignments_submission_rate"]'
        )
        self.start_date = self.locator.locator('[data-field="start_date"]')
        self.end_date = self.locator.locator('[data-field="end_date"]')
        self.assignments_count = self.locator.locator(
            '[data-field="assignments_count"][role="gridcell"]'
        )
        self.company_name = self.locator.locator('[data-field="company.name"]')

    def to_entity(self) -> EducationCampaignEntity:
        return EducationCampaignEntity(
            title=self.title.text_content(),
            assignments_submission_rate=self.assignments_submission_rate.text_content(),
            start_date=self.start_date.text_content(),
            end_date=self.end_date.text_content(),
            assignments_count=int(self.assignments_count.text_content()),
            company_name=self.company_name.text_content()
            if self.company_name.is_visible()
            else None,
        )
