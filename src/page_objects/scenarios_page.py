import allure
from playwright.sync_api import Page
from src.page_objects.base_page import BasePage
from src.models.scenario_model import ScenarioModel


class ScenariosPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_scenario = page.get_by_role("button", name="Create Scenario")

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
