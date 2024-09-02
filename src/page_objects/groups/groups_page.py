import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.groups import group_created_text
from src.page_objects.groups.create_group_page import CreateGroupPage


class GroupsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.upload_groups_button = self.page.get_by_role(
            'button', name='Upload Groups'
        )
        self.create_group_button = self.page.get_by_role('button', name='Create Group')
        self.search_input = self.page.get_by_role('insertion')
        self.upload_groups_component = UploadGroupsComponent(
            self.page.get_by_role(role='dialog')
        )

    @allure.step('GroupsPage: create {group_name} group')
    def create_group(
        self,
        group_name: str,
        managers_email: list[str] = None,
        employees_email: list[str] = None,
    ):
        self.create_group_button.click()
        create_group_page = CreateGroupPage(self.page)
        create_group_page.create_group(group_name, managers_email, employees_email)
        expect(self.alert_message).to_have_text(group_created_text)

    @allure.step('GroupsPage: upload file {file_path}')
    def upload_file(self, file_path: str):
        self.upload_groups_button.click()
        expect(self.upload_groups_component.locator).to_be_visible()
        with self.page.expect_file_chooser() as fc:
            self.upload_groups_component.upload_button.click()
            fc.value.set_files(file_path)
            expect(self.loading).to_be_visible()
            self.wait_for_loading_state()
            expect(self.upload_groups_component.locator).not_to_be_visible()


class UploadGroupsComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.upload_button = self.locator.get_by_text(
            'Or Select A File From Your Computer'
        )
        self.download_required_button = self.locator.get_by_text(
            'Download Required Fields CSV'
        )
