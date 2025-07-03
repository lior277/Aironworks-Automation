import tempfile

import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.table_element import Table
from src.page_objects.modify_campaign_page import ModifyCampaignPage


class CampaignDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # self.export_csv_button = self.page.get_by_role('button', name='Export CSV')
        self.summary_export_csv_button = self.page.get_by_role(
            'heading', name='Campaign Attacks Summary'
        ).locator('..//button[text()="Export CSV"]')
        self.url = self.default_url + 'admin/dashboard/attacks/executions/'
        self.table_campaign_attacks_summary = Table(
            page.locator(
                '//button[@id="more-button"]//ancestor::div[contains(@class,"MuiDataGrid-pinnedColumns")]/preceding-sibling::div//div[@role="row"]'
            ),
            CampaignAttacksSummary,
        )
        self.manage_campaign_button = self.page.get_by_role(
            'button', name='Manage Campaign'
        )
        self.modify_campaign_option = self.page.get_by_role(
            'menuitem', name='Modify Campaign'
        )

    @allure.step(
        'CampaignDetailsPage: open campaign detailed page for {campaign_id} campaign id'
    )
    def open(self, campaign_id: str):
        self.page.goto(self.url + campaign_id)
        expect(self.summary_export_csv_button).to_be_visible()
        self.summary_export_csv_button.scroll_into_view_if_needed()
        self.wait_for_progress_bar_disappears()
        self.wait_for_loading_state()
        return self

    @allure.step('CampaignDetailsPage: export csv')
    def export_csv(self):
        path = tempfile.mktemp(suffix='.csv')
        with self.page.expect_download() as download_info:
            self.summary_export_csv_button.click()
        download_event = download_info.value
        download_event.save_as(path)
        return path

    @allure.step('CampaignDetailsPage: navigate to modify campaign page')
    def navigate_to_modify_campaign_page(self):
        self.manage_campaign_button.click()
        self.modify_campaign_option.click()
        return ModifyCampaignPage(self.page)


class CampaignAttacksSummary:
    def __init__(self, locator: Locator):
        self.status = locator.locator('[data-field="status"]')
        self.opened = locator.locator('[data-field="open"]')
        self.date_clicked = locator.locator('[data-field="date_clicked"]')
        self.first_name = locator.locator('[data-field="target.first_name"]')
        self.last_name = locator.locator('[data-field="target.last_name"]')
        self.email = locator.locator('[data-field="target.email"]')
        self.user_agent = locator.locator('[data-field="user_agent"]')
        self.ip_address = locator.locator('[data-field="ip_address"]')
        self.report_time = locator.locator('[data-field="report_time"]')
        self.incident_time = locator.locator('[data-field="incident_time"]')
