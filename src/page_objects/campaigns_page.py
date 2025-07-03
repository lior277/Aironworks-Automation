import allure
from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.campaign_details_page import CampaignDetailsPage
from src.page_objects.data_types.table_element import Table


class CampaignsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.default_url + 'admin/dashboard/attacks/executions/'
        self.ongoing_campaigns_table = Table(
            self.page.locator('.MuiDataGrid-row').nth(1), OngoingCampaignTableComponent
        )

    def click_first_ongoing_campaign(self):
        self.ongoing_campaigns_table.get_row_by_index(0).strategy.click()
        return CampaignDetailsPage(self.page)

    @allure.step('CampaignsPage: wait for tables load')
    def wait_for_tables_load(self):
        self.wait_for_progress_bar_disappears()
        self.wait_for_loading_state()


class OngoingCampaignTableComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.status = self.locator.locator('[data-field="status"]')
        self.strategy = self.locator.locator('[data-field="strategy_name"]')
        self.attack_vector = self.locator.locator('[data-field="vector"]')
        self.date = self.locator.locator('[data-field="date_created"]')
