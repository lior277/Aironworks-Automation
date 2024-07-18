import allure
from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.education_campaign import (
    confirm_deletion_body_text,
    education_campaign_deleted_text,
)


class EducationCampaignDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.delete_button = self.page.get_by_text("Delete Campaign")
        self.title_txt = self.page.get_by_role("heading", level=4)
        self.delete_campaign_title = self.page.get_by_role("heading", level=2)
        self.delete_campaign_body = self.page.locator(selector=".MuiDialogContent-root")
        self.confirm_delete_button = self.page.get_by_text("Yes, Delete Campaign")
        self.cancel_button = self.page.get_by_text("Cancel")

    @allure.step("EducationCampaignDetailsPage: delete education campaign")
    def delete_campaign(self):
        self.delete_button.click()
        self.delete_campaign_title.wait_for()
        expect(self.delete_campaign_body).to_have_text(confirm_deletion_body_text)
        self.confirm_delete_button.click()
        expect(self.alert_message.first).to_contain_text(education_campaign_deleted_text)
