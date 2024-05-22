from playwright.sync_api import Page
import tempfile
from src.page_objects.base_page import BasePage


class CampaignDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.export_csv_button = self.page.get_by_role("button", name="Export CSV")

    def export_csv(self):
        path = tempfile.mktemp(suffix=".csv")
        with self.page.expect_download() as download_info:
            self.export_csv_button.click()
        download_event = download_info.value
        download_event.save_as(path)
        return path
