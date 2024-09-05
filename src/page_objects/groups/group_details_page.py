import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.groups import group_is_deleted_text


class GroupDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.title = self.page.get_by_role('heading', level=4)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.delete_group_button = self.page.get_by_role('button', name='Delete Group')
        self.edit_group_button = self.page.get_by_role('button', name='Edit Group')
        self.delete_group_component = DeleteGroupComponent(
            self.page.get_by_role('presentation')
        )

    @allure.step('GroupDetailsPage: delete group')
    def delete_group(self):
        self.delete_group_button.click()
        self.delete_group_component.locator.wait_for()
        self.delete_group_component.delete_button.click()
        self.wait_for_progress_bar_disappears()
        expect(self.alert_message).to_have_text(group_is_deleted_text)


class DeleteGroupComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.get_by_role('heading', level=2)
        self.cancel_button = self.locator.get_by_role('button', name='Cancel')
        self.delete_button = self.locator.get_by_role('button', name='Delete')
