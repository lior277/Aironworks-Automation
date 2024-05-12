import allure
import time
import re
from typing import Literal
from playwright.sync_api import Page, expect
from src.page_objects.base_page import BasePage
from src.models.scenario_model import ScenarioModel


class ScenariosPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_scenario_button = page.get_by_role("button", name="Create Scenario")
        self.visible_tab = page.get_by_role("tab", name="Visible")
        self.hide_scenario = page.get_by_role("button", name="Hide")
        self.search = self.page.get_by_placeholder("Search by Name")
        self.scenarios_list = self.page.locator(".MuiGrid-root > .MuiBox-root")

        # scenario wizard
        self.scenario_name = self.page.get_by_role("textbox", name="Scenario Name")
        self.sender_address = self.page.get_by_role("textbox", name="Sender Address")
        self.sender_name = self.page.get_by_role("textbox", name="Sender Name")
        self.subject = self.page.get_by_role("textbox", name="Subject")
        self.url_suffix = self.page.get_by_role("textbox", name="URL Suffix")
        self.next = self.page.get_by_role("button", name="Next")
        self.html_content = self.page.get_by_label("Editor editing area: main")
        self.save = self.page.get_by_role("button", name="Save")

    @allure.step("ScenariosPage: navigate to create scenario")
    def navigate_create_scenario(self):
        self.create_scenario_button.click()
        self.page.wait_for_load_state(timeout=5)

    @allure.step("ScenariosPage: filter by name")
    def filter_by_name(self, name):
        self.search.fill(name)

    @allure.step("ScenariosPage: filter by language")
    def filter_by_language(self, language: Literal["All", "English", "Japanese"]):
        self.page.get_by_label("Language", exact=True).click()
        self.page.get_by_label(language).click()

    @allure.step("ScenariosPage: wait for filters to sync")
    def wait_sync_filters(self):
        time.sleep(
            1
        )  # this page displays the old results for a brief moment before hiding it so unfortunatly we need to sleep a bit

    @allure.step("ScenariosPage: finish draft")
    def finish_draft(self):
        self.page.get_by_role("button", name="Finish Draft").click()
        self.page.get_by_role("button", name="OK").click()
        self.page.wait_for_load_state(timeout=5)

    @allure.step("ScenariosPage: submit create scenario form")
    def submit_create_scenario_form(self, scenario: ScenarioModel, clone_mode=False):
        self.scenario_name.fill(scenario.name)
        self.sender_address.fill(scenario.sender_address)

        domain_buttons = self.page.get_by_role("button", name="Domain").all()
        sender_domain = domain_buttons[0]
        link_domain = domain_buttons[1]

        sender_domain.click()
        self.page.get_by_role("option", name=scenario.sender_domain).click()

        self.sender_name.fill(scenario.sender_name)
        self.subject.fill(scenario.subject)
        link_domain.click()
        self.page.get_by_role("option", name=scenario.link_domain).click()
        self.url_suffix.fill(scenario.url_suffix)

        self.next.click()
        if clone_mode:
            self.page.get_by_role("button", name="New Body").click()
            self.page.wait_for_load_state(timeout=5)
        self.html_content.fill(scenario.html_content)
        self.save.click()
        self.page.wait_for_load_state(timeout=5)

    def get_visible_results(self):
        return self.scenarios_list.get_by_role("button").all()

    @allure.step("ScenariosPage: Create scenario")
    def create_scenario(self, scenario: ScenarioModel):
        self.navigate_create_scenario()

        self.submit_create_scenario_form(scenario)

        expect(self.page.get_by_text("Created new scenario")).to_be_visible()

    @allure.step("Find scenario")
    def find_scenario(self, scenario_name: str):
        self.filter_by_name(scenario_name)
        self.filter_by_language("All")
        self.wait_sync_filters()
        scenario = (
            self.page.get_by_role("button")
            .filter(has_text=re.compile(scenario_name))
            .first
        )
        expect(scenario).to_be_visible()
        return scenario
