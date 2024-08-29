import allure
from playwright.sync_api import Page, expect

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
