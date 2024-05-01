import allure
import time
from typing import Literal
from playwright.sync_api import Page
from src.page_objects.base_page import BasePage
from src.models.scenario_model import ScenarioModel


class ScenariosPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_scenario = page.get_by_role("button", name="Create Scenario")
        self.visible_tab = page.get_by_role("tab", name="Visible")
        self.hide_scenario = page.get_by_role("button", name="Hide")
        self.search = self.page.get_by_placeholder("Search by Name")

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
        self.create_scenario.click()
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
    def submit_create_scenario_form(self, scenario: ScenarioModel):
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
        self.html_content.fill(scenario.html_content)
        self.save.click()
        self.page.wait_for_load_state(timeout=5)
