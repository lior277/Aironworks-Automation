import re
import time
from typing import Literal

import allure
from playwright.sync_api import Locator, Page, expect

from src.models.scenario import CampaignType, ScenarioCloneMode, TargetType
from src.models.scenario_model import ScenarioModel
from src.page_objects.base_page import BasePage
from src.page_objects.const import (
    created_new_scenario_text,
    deleted_scenario_text,
    invalid_file_type_text,
    marked_attack_non_draft_message,
    scenario_file_name_helper_text,
)
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.execute_campaign_page import ExecuteCampaignPage
from src.page_objects.request_ai_scenario_page import RequestAiScenarioPage


class ScenariosPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.choose_edit_mode_window = ChooseEditModeComponent(
            self.page.get_by_label('Choose Edit Mode')
        )
        self.create_scenario_button = page.get_by_role('button', name='Create Scenario')
        self.request_ai_generated_button = page.get_by_role('button').filter(
            has_text='Request an AI Generated Scenario'
        )
        self.visible_tab = page.get_by_role('tab', name='Visible')
        self.hide_scenario = page.get_by_role('button', name='Hide', exact=True)
        self.execute = page.get_by_role('button', name='Create Campaign')
        self.search = self.page.get_by_placeholder('Search by Name')
        self.scenarios_list = self.page.locator('.MuiGrid-root > .MuiBox-root')

        # scenario wizard
        self.scenario_name = self.page.get_by_role('textbox', name='Scenario Name')
        self.vector_dropdown = DropDown(
            link_locator=self.page.locator('//div[@id="vector"]'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.sender_address = self.page.get_by_role('textbox', name='Sender Address')
        self.sender_name = self.page.get_by_role('textbox', name='Sender Name')
        self.subject = self.page.get_by_role('textbox', name='Subject')

        # target details(Only for AW Admin)
        self.employee_attack = self.page.get_by_role('button', name='Employee Attack')
        self.company_attack = self.page.get_by_role('button', name='Company Attack')
        self.general = self.page.get_by_role('button', name='General')
        self.targeted = self.page.get_by_role('button', name='Targeted')
        self.target_company_dropdown = DropDown(
            link_locator=self.page.locator(
                '//h6[text()="Target Details"]/..'
            ).get_by_role('combobox', name='Target Company'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        # self.target_company = self.page.get_by_role('combobox', name='Target Company')

        self.url_suffix = self.page.get_by_role('textbox', name='URL Suffix')

        self.next = self.page.get_by_role('button', name='Next')
        self.show_preview_button = self.page.get_by_role('button', name='Show Preview')
        self.html_content = self.page.get_by_label('Editor editing area: main')
        self.content = self.page.get_by_role('textbox', name='Content')
        self.save = self.page.get_by_role('button', name='Save')
        self.sender_domain_dropdown = DropDown(
            link_locator=self.page.locator(
                '//h6[text()="Source Details"]/..'
            ).get_by_role('combobox', name='Domain'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.link_domain_dropdown = DropDown(
            link_locator=self.page.locator(
                '//h6[text()="Base Attack URL"]/..'
            ).get_by_role('combobox', name='Domain'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.phishing_link_button = self.page.locator('[value="LINK"]')
        self.data_entry_button = self.page.locator('[value="DATAENTRY"]')
        self.attachment_button = self.page.locator('[value="ATTACHMENT"]')
        self.upload_pdf_file_button = self.page.get_by_role(
            'button', name='Upload Attachment File'
        )
        self.delete_file_button = self.page.get_by_label('delete-file')
        self.file_name_input = self.page.locator(
            '[aria-describedby="file-name-helper-text"]'
        )
        self.file_name_helper_text = self.page.locator('[id="file-name-helper-text"]')
        self.data_entry_dropdown = DropDown(
            self.page.get_by_role('combobox', name='Login Page Type'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.first_scenario = (
            self.page.get_by_role('list').locator('//div[@role="button"]').nth(1)
        )
        self.delete_button = self.page.get_by_role('button', name='Delete')
        self.confirm_delete_button = self.page.get_by_role(
            'generic', name='Delete Attack'
        ).get_by_role('button', name='Delete')

    @allure.step('ScenariosPage: navigate to create scenario')
    def navigate_create_scenario(self):
        self.create_scenario_button.click()
        self.scenario_name.wait_for()

    @allure.step('ScenariosPage: navigate to request AI generated scenario')
    def navigate_request_ai_generated_scenario(self):
        self.request_ai_generated_button.click()
        return RequestAiScenarioPage(self.page)

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
        self.ensure_alert_message_is_visible(
            marked_attack_non_draft_message, timeout=30_000
        )

    @allure.step('ScenariosPage: select target details')
    def select_target_details(self, scenario: ScenarioModel):
        match scenario.target_details.target_type:
            case TargetType.EMPLOYEE:
                self.employee_attack.click()
            case TargetType.COMPANY:
                self.company_attack.click()
        if scenario.target_details.target_company:
            # self.targeted.click()
            self.target_company_dropdown.select_item_by_text(
                scenario.target_details.target_company
            )

    @allure.step('ScenariosPage: submit create {scenario} scenario form')
    def submit_create_scenario_form(
        self, scenario: ScenarioModel, clone_mode: ScenarioCloneMode = None
    ):
        self.scenario_name.fill(scenario.vector + ' ' + scenario.name)
        self.vector_dropdown.select_item_by_text(scenario.vector)
        if scenario.vector == 'Email':
            self.sender_address.fill(scenario.sender_address)
            self.sender_domain_dropdown.select_item_by_text(
                scenario.sender_domain, loading_text='Loading...', timeout=15_000
            )
            self.subject.fill(scenario.subject)
            self.select_content_type(scenario)
        self.sender_name.fill(scenario.sender_name)

        if scenario.target_details:
            self.select_target_details(scenario)

        self.link_domain_dropdown.select_item_by_text(
            scenario.link_domain, loading_text='Loading...', timeout=15_000
        )
        self.url_suffix.fill(scenario.url_suffix)
        self.next.click()
        if clone_mode:
            self.choose_edit_mode_window.select_clone_mode(clone_mode)
            self.wait_for_progress_bar_disappears()
        if (
            scenario.vector == 'Email'
            and scenario.html_content
            and not clone_mode
            or clone_mode == ScenarioCloneMode.NEW_BODY
        ):
            expect(self.html_content).to_be_empty()
            self.html_content.fill(scenario.html_content + scenario.custom_text)
            self.show_preview_button.click()
            time.sleep(10)
            self.preview_text = self.page.locator(
                'iframe[title="my frame"]'
            ).content_frame.locator('body')
            expect(self.preview_text).to_contain_text(scenario.custom_text)
            self.page.keyboard.press('Escape')
        if scenario.vector == 'SMS' and scenario.html_content:
            expect(self.content).to_be_empty()
            self.content.fill(scenario.html_content + scenario.custom_text_web_sms)
            self.show_preview_button.click()
            time.sleep(10)
            self.preview_text = (
                self.page.get_by_role('dialog', name='SMS Attack Preview')
                .locator('.css-1nqjmf3')
                .get_by_role('paragraph')
            )
            trimmed_preview_text = re.sub(r'\s+', '', self.preview_text.text_content())
            trimmed_custom_text = re.sub(r'\s+', '', scenario.custom_text_web_sms)
            trimmed_custom_text = trimmed_custom_text.replace('←', '<-')
            trimmed_preview_text = trimmed_preview_text.replace('←', '<-')
            print(f'trimmed_preview_text: {trimmed_preview_text}')
            print(f'trimmed_custom_text: {trimmed_custom_text}')
            # expect(self.preview_text).to_contain_text(scenario.custom_text)
            assert trimmed_custom_text in trimmed_preview_text
            self.page.keyboard.press('Escape')
        if scenario.vector == 'Web' and scenario.html_content:
            expect(self.content).to_be_empty()
            self.content.fill(scenario.html_content + scenario.custom_text_web_sms)
            self.show_preview_button.click()
            time.sleep(10)
            self.preview_text = (
                self.page.get_by_role('dialog', name='Web Attack Preview')
                .locator('.css-1nqjmf3')
                .get_by_role('paragraph')
            )
            trimmed_preview_text = re.sub(r'\s+', '', self.preview_text.text_content())
            trimmed_custom_text = re.sub(r'\s+', '', scenario.custom_text_web_sms)
            # expect(self.preview_text).to_contain_text(scenario.custom_text)
            assert trimmed_custom_text in trimmed_preview_text
            self.page.keyboard.press('Escape')
        self.save.click()
        self.wait_for_progress_bar_disappears(timeout=30_000)

    def get_visible_results(self):
        return self.scenarios_list.get_by_role('button').all()

    @allure.step('ScenariosPage: Delete scenario')
    def delete_scenario(self):
        self.first_scenario.click()
        self.delete_button.click()
        self.delete_button.click()
        self.ensure_alert_message_is_visible(deleted_scenario_text)

    @allure.step('ScenariosPage: Create scenario {scenario}')
    def create_scenario(self, scenario: ScenarioModel):
        self.navigate_create_scenario()
        self.submit_create_scenario_form(scenario)
        self.ensure_alert_message_is_visible(created_new_scenario_text)

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

    @allure.step('ScenariosPage: select campaign type')
    def select_content_type(self, scenario: ScenarioModel):
        match scenario.campaign_type:
            case (
                CampaignType.DATA_ENTRY_APPLE
                | CampaignType.DATA_ENTRY_MICROSOFT
                | CampaignType.DATA_ENTRY_GOOGLE
            ):
                self.data_entry_button.check()
                self.data_entry_dropdown.select_item_by_text(
                    scenario.campaign_type.value
                )
            case CampaignType.ATTACHMENT:
                self.attachment_button.check()
                with self.page.expect_file_chooser() as fc:
                    self.upload_pdf_file_button.click()
                    fc.value.set_files(scenario.file_path)
                    self.wait_for_progress_bar_disappears()
                    if scenario.file_path.endswith('.pdf'):
                        expect(self.delete_file_button).to_be_visible()
                        expect(self.file_name_helper_text).to_have_text(
                            scenario_file_name_helper_text
                        )
                    else:
                        self.ensure_alert_message_is_visible(invalid_file_type_text)
                        expect(self.delete_file_button).not_to_be_visible()
            case _:
                self.phishing_link_button.check()

    @allure.step('ScenariosPage: verify cloned {scenario} scenario form')
    def verify_cloned_scenario_form(self, scenario: ScenarioModel):
        expect(self.scenario_name).to_have_attribute(
            name='value', value=scenario.vector + ' ' + scenario.name
        )
        expect(self.sender_address).to_have_attribute(
            name='value', value=scenario.sender_address
        )
        expect(self.sender_domain_dropdown.locator).to_have_text(scenario.sender_domain)
        expect(self.sender_name).to_have_attribute(
            name='value', value=scenario.sender_name
        )
        expect(self.subject).to_have_attribute(name='value', value=scenario.subject)
        expect(self.link_domain_dropdown.locator).to_have_text(scenario.link_domain)
        expect(self.url_suffix).to_have_attribute(
            name='value', value=scenario.url_suffix
        )
        match scenario.campaign_type:
            case CampaignType.PHISHING_LINK:
                expect(self.phishing_link_button).to_be_checked()
            case CampaignType.ATTACHMENT:
                expect(self.attachment_button).to_be_checked()
            case _:
                expect(self.data_entry_button).to_be_checked()


class ChooseEditModeComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.new_body_button = self.locator.get_by_role('button', name='New Body')
        self.copy_content_button = self.locator.get_by_role(
            'button', name='Copy Content'
        )

    @allure.step('ChooseEditModeComponent: select {clone_mode} clone mode')
    def select_clone_mode(self, clone_mode: ScenarioCloneMode = None):
        match clone_mode:
            case ScenarioCloneMode.COPY_CONTENT:
                self.copy_content_button.click()
            case _:
                self.new_body_button.click()
