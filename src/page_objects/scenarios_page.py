import re
from typing import Literal

import allure
from playwright.sync_api import Page, expect

from src.models.scenario_model import ScenarioModel
from src.page_objects import created_new_scenario_text, marked_attack_non_draft_message
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.execute_campaign_page import ExecuteCampaignPage


class ScenariosPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_scenario_button = page.get_by_role('button', name='Create Scenario')
        self.visible_tab = page.get_by_role('tab', name='Visible')
        self.hide_scenario = page.get_by_role('button', name='Hide', exact=True)
        self.execute = page.get_by_role('button', name='Execute')
        self.search = self.page.get_by_placeholder('Search by Name')
        self.scenarios_list = self.page.locator('.MuiGrid-root > .MuiBox-root')

        # scenario wizard
        self.scenario_name = self.page.get_by_role('textbox', name='Scenario Name')
        self.sender_address = self.page.get_by_role('textbox', name='Sender Address')
        self.sender_name = self.page.get_by_role('textbox', name='Sender Name')
        self.subject = self.page.get_by_role('textbox', name='Subject')
        self.url_suffix = self.page.get_by_role('textbox', name='URL Suffix')
        self.next = self.page.get_by_role('button', name='Next')
        self.html_content = self.page.get_by_label('Editor editing area: main')
        self.save = self.page.get_by_role('button', name='Save')
        self.sender_domain_dropdown = DropDown(
            link_locator=self.page.locator(
                '//h6[text()="Source Details"]/..'
            ).get_by_role('button', name='Domain'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.link_domain_dropdown = DropDown(
            link_locator=self.page.locator(
                '//h6[text()="Base Attack URL"]/..'
            ).get_by_role('button', name='Domain'),
            option_list_locator=self.page.locator('[role="option"]'),
        )

    @allure.step('ScenariosPage: navigate to create scenario')
    def navigate_create_scenario(self):
        self.create_scenario_button.click()
        self.scenario_name.wait_for()

    @allure.step('ScenariosPage: filter by name')
    def filter_by_name(self, name):
        self.search.fill(name)

    @allure.step('ScenariosPage: filter by language')
    def filter_by_language(self, language: Literal['All', 'English', 'Japanese']):
        self.page.get_by_label('Language', exact=True).click()
        self.page.get_by_label(language).click()

    @allure.step('ScenariosPage: finish draft')
    def finish_draft(self):
        self.page.get_by_role('button', name='Finish Draft').click()
        self.page.get_by_role('button', name='OK').click()
        expect(self.alert_message.first).to_contain_text(
            marked_attack_non_draft_message
        )

    @allure.step('ScenariosPage: submit create scenario form')
    def submit_create_scenario_form(self, scenario: ScenarioModel, clone_mode=False):
        self.scenario_name.fill(scenario.name)
        self.sender_address.fill(scenario.sender_address)
        self.sender_domain_dropdown.select_item_by_text(scenario.sender_domain)
        self.sender_name.fill(scenario.sender_name)
        self.subject.fill(scenario.subject)
        self.link_domain_dropdown.select_item_by_text(scenario.link_domain)
        self.url_suffix.fill(scenario.url_suffix)

        self.next.click()
        if clone_mode:
            self.page.get_by_role('button', name='New Body').click()
            self.wait_for_progress_bar_disappears()
        self.html_content.fill(scenario.html_content)
        self.save.click()
        self.wait_for_progress_bar_disappears(timeout=30_000)

    def get_visible_results(self):
        return self.scenarios_list.get_by_role('button').all()

    @allure.step('ScenariosPage: Create scenario {scenario}')
    def create_scenario(self, scenario: ScenarioModel):
        self.navigate_create_scenario()
        self.submit_create_scenario_form(scenario)
        expect(self.alert_message.first).to_contain_text(created_new_scenario_text)

    @allure.step('Find scenario by {scenario_name} name')
    def find_scenario(self, scenario_name: str):
        self.filter_by_name(scenario_name)
        self.filter_by_language('All')
        self.wait_for_progress_bar_disappears(timeout=30_000)
        scenario = (
            self.page.get_by_role('button')
            .filter(has_text=re.compile(scenario_name))
            .first
        )
        expect(scenario).to_be_visible()
        return scenario

    @allure.step('ScenariosPage: Execute scenario')
    def execute_scenario(self) -> ExecuteCampaignPage:
        self.execute.click()
        return ExecuteCampaignPage(self.page)
