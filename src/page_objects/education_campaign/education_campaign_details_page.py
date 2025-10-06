import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.filter import Filter
from src.page_objects.data_types.table_element import Table
from src.page_objects.education_campaign.const import (
    confirm_deletion_body_text,
    education_campaign_deleted_text,
)


class EducationCampaignDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.default_url + 'admin/dashboard/education-campaigns/view/'
        self.manage_campaign_button = self.page.get_by_role(
            'button', name='Manage Campaign'
        )
        self.delete_cmapaign_option = self.page.get_by_role(
            'menuitem', name='Delete Campaign'
        )
        self.title_txt = self.page.get_by_role('heading', level=4).nth(1)
        self.delete_campaign_title = self.page.get_by_role('heading', level=2)
        self.delete_campaign_body = self.page.locator(selector='.MuiDialogContent-root')
        self.confirm_delete_button = self.page.get_by_text('Yes, Delete Campaign')
        self.cancel_button = self.page.get_by_text('Cancel')
        self.assignment_list = Table(
            self.page.locator(
                '//h6[text()="Assignments List"]//following-sibling::div//div[@role="rowgroup"]/div'
            ),
            AssignmentList,
        )
        self.assignment_list_filter = Filter(
            self.page.get_by_role('button', name='Show filters').nth(0),
            self.page.get_by_role('combobox', name='Columns'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
            self.page.get_by_role('presentation'),
        )

    @allure.step('EducationCampaignDetailsPage: delete education campaign')
    def delete_campaign(self):
        self.manage_campaign_button.click()
        expect(self.delete_cmapaign_option).to_be_visible()
        self.delete_cmapaign_option.click()
        self.delete_campaign_title.wait_for()
        expect(self.delete_campaign_body).to_have_text(confirm_deletion_body_text)
        self.confirm_delete_button.click()
        self.ensure_alert_message_is_visible(education_campaign_deleted_text)

    @allure.step(
        'CampaignDetailsPage: open campaign detailed page for {campaign_id} campaign id'
    )
    def open(self, campaign_id: str):
        self.page.goto(self.url + campaign_id)
        self.wait_for_progress_bar_disappears()
        self.wait_for_loading_state()
        return self

    @allure.step(
        'EducationCampaignDetailsPage: filter assignment list by {field} = {value}'
    )
    def filter_assignments(self, field: str, value: str, number_record: int):
        self.assignment_list_filter.filter_by(field, value)
        expect(self.assignment_list._Table__locator).to_have_count(
            number_record, timeout=30000
        )


class AssignmentList:
    def __init__(self, locator: Locator):
        self.status = locator.locator('[data-field="status"]')
        self.opened = locator.locator('[data-field="open"]')
        self.completion_date = locator.locator('[data-field="date_submitted"]')
        self.first_name = locator.locator('[data-field="customer.first_name"]')
        self.last_name = locator.locator('[data-field="customer.last_name"]')
        self.email = locator.locator('[data-field="customer.email"]')
        self.language = locator.locator('[data-field="customer.language"]')
        self.position = locator.locator('[data-field="customer.fields.Position"]')
        self.url = locator.locator('[data-field="assignment_url"]')
