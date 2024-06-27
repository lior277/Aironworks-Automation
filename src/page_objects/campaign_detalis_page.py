import tempfile

from playwright.sync_api import Page

from src.page_objects.base_page import BasePage


class CampaignDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.export_csv_button = self.page.get_by_role("button", name="Export CSV")
        self.url = self.default_url + "admin/dashboard/attacks/executions/"

    def open_campaign_detailed_page(self, campaign_id: str):
        self.page.goto(self.url + campaign_id)
        self.wait_for_progress_bar_disappears()

    def export_csv(self):
        path = tempfile.mktemp(suffix=".csv")
        with self.page.expect_download() as download_info:
            self.export_csv_button.click()
        download_event = download_info.value
        download_event.save_as(path)
        return path
