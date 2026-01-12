import allure
from playwright.sync_api import Page, expect

from src.models.automatic_campaign_model import AutomaticCampaignModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.data_types.filter import Filter
from src.page_objects.operations.const import create_automatic_campaign_successful_text

from ..employee_table_component import EmployeeTableComponent


class CreateAutomaticCampaignPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.bread_crumb = self.page.get_by_label('current-breadcrumb')
        self.cancel_button = self.page.get_by_text('Cancel')
        self.preview_button = self.page.get_by_role(
            'button', name='Preview', exact=True
        )
        self.launch_button = self.page.get_by_role('button', name='Launch', exact=True)
        self.operation_name_input = self.page.get_by_role(
            'textbox', name='Operation Name'
        )
        self.vector_type_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Vector Type'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.select_scenario_button = self.page.get_by_role(
            'button', name='Select Scenario'
        )
        # Select Targets
        self.random_sample_button = self.page.get_by_role(
            'button', name='+ Random Sample'
        )
        self.pick_employees_button = self.page.get_by_role(
            'button', name='+ Pick Employees'
        )
        self.pick_groups_button = self.page.get_by_role('button', name='+ Pick Groups')
        self.pick_previous_successful_employees_button = self.page.get_by_role(
            'button', name='+ Pick Previously Successfully Attacked Employees'
        )
        self.employee_table = EmployeeTableComponent(page.get_by_test_id('table'), page)
        self.filter = Filter(
            self.page.locator('//button[contains(text(),"Filters")]'),
            self.page.get_by_role('combobox', name='Columns'),
            self.page.locator('[placeholder="Filter value"]'),
            self.page.locator('[data-testid="LoadIcon"]'),
            self.page.get_by_role('presentation'),
        )
        # Parameters
        self.execution_date_input = self.page.get_by_role(
            'textbox', name='Execution date'
        )
        self.completion_date_input = self.page.get_by_role(
            'textbox', name='Completion date'
        )
        self.frequency_input = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Frequency'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.scenarios_employee_input = self.page.get_by_role(
            'spinbutton', name='Scenarios per employee'
        )
        self.campaign_duration_input = self.page.get_by_role(
            'spinbutton', name='Single campaign duration (days)'
        )
        self.range_start_time_input = self.page.get_by_role(
            'textbox', name='Range start time'
        )
        self.range_end_time_input = self.page.get_by_role(
            'textbox', name='Range end time'
        )

        self.interval_input = self.page.get_by_role(
            'spinbutton', name='Time interval(days)'
        )

        self.select_education_content_button = self.page.get_by_role(
            'button', name='Select Education Content'
        )
        self.select_education_survey_button = self.page.get_by_role(
            'button', name='Select Education Survey'
        )

    @allure.step('CreateAutomaticCampaignPage: create automatic campaign')
    def create_automatic_campaign(self, automatic_campaign: AutomaticCampaignModel):
        self.operation_name_input.fill(automatic_campaign.operation_name)
        self.vector_type_dropdown.select_item_by_text(automatic_campaign.vector_type)
        self.select_scenarios(automatic_campaign.scenarios[0])
        self.pick_employees_button.click()
        expect(self.employee_table.table).to_be_visible()
        self.filter.filter_by('Email', automatic_campaign.employees[0])
        self.employee_table.get_employee_row(
            automatic_campaign.employees[0]
        ).select_row()
        self.execution_date_input.fill(automatic_campaign.execution_date)
        self.completion_date_input.fill(automatic_campaign.completion_date)
        self.frequency_input.select_item_by_text(automatic_campaign.frequency)
        self.scenarios_employee_input.fill(automatic_campaign.scenarios_employee)
        self.campaign_duration_input.fill(automatic_campaign.campaign_duration)
        self.range_start_time_input.fill(automatic_campaign.range_start_time)
        self.range_end_time_input.fill(automatic_campaign.range_end_time)
        self.interval_input.fill(automatic_campaign.interval)
        self.select_content(automatic_campaign.content)
        self.select_survey(automatic_campaign.survey)
        self.preview_button.click()
        self.launch_button.click()
        expect(self.alert_message).to_have_text(
            create_automatic_campaign_successful_text
        )

    @allure.step('CreateAutomaticCampaignPage: select scenario')
    def navigate_to_select_scenario_page(self):
        self.select_scenario_button.click()
        return SelectScenarioPage(self.page)

    @allure.step('CreateAutomaticCampaignPage: navigate to select content page')
    def navigate_to_select_content_page(self):
        self.select_education_content_button.click()
        return SelectContentSurveyPage(self.page)

    @allure.step('CreateAutomaticCampaignPage: navigate to select survey page')
    def navigate_to_select_survey_page(self):
        self.select_education_survey_button.click()
        return SelectContentSurveyPage(self.page)

    @allure.step('CreateAutomaticCampaignPage: select scenarios')
    def select_scenarios(self, name: str):
        select_scenario_page = self.navigate_to_select_scenario_page()
        select_scenario_page.select_two_scenarios(name)

    @allure.step('CreateAutomaticCampaignPage: select content')
    def select_content(self, name: str):
        select_content_page = self.navigate_to_select_content_page()
        select_content_page.select_content(name)
        return select_content_page

    @allure.step('CreateAutomaticCampaignPage: select survey')
    def select_survey(self, name: str):
        select_survey_page = self.navigate_to_select_survey_page()
        select_survey_page.select_content(name)
        return select_survey_page


class SelectScenarioPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.next_button = self.page.get_by_role('button', name='Next', exact=True)
        self.search_by_name_input = self.page.get_by_role(
            'textbox', name='Search by Name'
        )
        self.scenario_cards = self.page.get_by_label('selectable-multi-card')

    def filter_by_name(self, name: str):
        self.search_by_name_input.fill(name)
        expect(
            self.scenario_cards.first.get_by_role('heading', level=6, name=name)
        ).to_contain_text(name)
        expect(
            self.scenario_cards.nth(1).get_by_role('heading', level=6, name=name)
        ).to_contain_text(name)

    def select_two_scenarios(self, name: str):
        self.filter_by_name(name)
        self.scenario_cards.first.get_by_role('checkbox').check()
        self.scenario_cards.nth(1).get_by_role('checkbox').check()
        self.page.get_by_text('2 scenarios selected').wait_for()
        self.next_button.click()


class SelectContentSurveyPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.back_button = self.page.get_by_role('button', name='Back')
        self.next_button = self.page.get_by_role('button', name='Next', exact=True)
        self.search_by_name_input = self.page.get_by_role(
            'textbox', name='Search by Content Name'
        )
        self.content_cards = self.page.get_by_label('content-card')

    def filter_by_name(self, name: str):
        self.search_by_name_input.fill(name)
        expect(
            self.content_cards.first.get_by_role('heading', level=3, name=name)
        ).to_contain_text(name)

    def select_content(self, name: str):
        self.filter_by_name(name)
        self.content_cards.first.click()
        self.next_button.click()
