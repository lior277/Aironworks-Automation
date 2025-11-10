from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown


class RequestAiScenarioPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.generate_scenario_button = page.get_by_role(
            'button', name='Generate Scenario'
        )
        self.preview_scenario_button = page.get_by_role(
            'button', name='Preview Scenario'
        )
        self.cancel_button = page.get_by_role('button', name='Cancel')
        self.vector_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Vector'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.scenarios_requested_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Scenarios Requested'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.attack_level_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Attack Level'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.language_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Language', exact=True),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.sender_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Sender'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.real_name_used_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Real Name Used'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.additional_info_text_area = page.get_by_role(
            'textbox', name='Add here any extra information or specific instructions.'
        )
        self.preview_popup = PreviewPopup(
            self.page.get_by_role('dialog', name='Modify Request')
        )

    def generate_scenario(
        self,
        number_of_scenarios: str,
        level: str,
        lannguage: str,
        sender: str,
        real_name: str,
        additional_info: str = 'Make sure to generate {{attack_url}} with a space behind',
    ):
        self.scenarios_requested_dropdown.select_item_by_text(number_of_scenarios)
        self.attack_level_dropdown.select_item_by_text(level)
        self.language_dropdown.select_item_by_text(lannguage)
        self.sender_dropdown.select_item_by_text(sender)
        self.real_name_used_dropdown.select_item_by_text(real_name)
        self.additional_info_text_area.fill(additional_info)
        self.generate_scenario_button.click()
        self.wait_for_progress_bar_disappears()
        self.preview_popup.choose_scenario_button.click()
        self.wait_for_loading_state()


class PreviewPopup:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.modify_request_button = self.locator.get_by_role(
            'button', name='Modify Request'
        )
        self.choose_scenario_button = self.locator.get_by_role(
            'button', name='Choose Scenario'
        )
        self.request_targeted_scenario_button = self.locator.get_by_role(
            'button', name='Request Targeted Scenario'
        )
