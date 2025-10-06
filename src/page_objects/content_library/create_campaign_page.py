import allure
from playwright.sync_api import Locator, Page, expect

from src.page_objects.base_page import BasePage
from src.page_objects.content_library.const import created_education_campaign_text
from src.page_objects.content_library.content_selection_page import ContentSelectionPage
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.data_types.table_element import Table


class CreateCampaignPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = (
            self.default_url
            + 'admin/dashboard/content-library/{content_library_id}/create-campaign'
        )
        self.create_button = self.page.get_by_role('button', name='Create')
        self.cancel_button = self.page.get_by_role('button', name='Cancel')
        self.show_filters_button = self.page.get_by_label('Show filters')
        self.target_employees_drop_down = DropDown(
            self.page.locator('[aria-labelledby="employee_option-label"]'),
            option_list_locator=page.locator('[role="option"]'),
        )
        self.target_company_drop_down = DropDown(
            self.page.locator('[id="target_company"]'),
            option_list_locator=page.locator('[role="option"]'),
        )

        self.table_specific_employees = Table(
            page.locator('//div[contains(@class,"MuiDataGrid-row")]'), SpecificEmployees
        )
        self.select_education_contents_button = self.page.get_by_role(
            'button', name='Select Education Content(S)'
        )
        self.campaign_name_input = self.page.get_by_role(
            'textbox', name='Campaign Name'
        )

    @allure.step(
        'CreateCampaignPage: open create campaign page for {content_library_id} content library'
    )
    def open(self, content_library_id: str):
        self.page.goto(self.url.format(content_library_id=content_library_id))
        self.create_button.wait_for(timeout=20000, state='visible')
        return self

    @allure.step('CreateCampaignPage: select targets')
    def select_targets(self):
        if self.target_company_drop_down.locator.is_visible():
            self.target_company_drop_down.select_item_by_text(
                'QA Accounts', search=True
            )
        self.target_employees_drop_down.select_item_by_text('Specific Employees')
        self.wait_for_loading_state()
        specific_employees = self.table_specific_employees.get_content()
        assert len(specific_employees) > 0, 'no any employees to select'
        specific_employees[0].check_box.set_checked(True)
        expect(specific_employees[0].check_box).to_be_checked(checked=True)

    @allure.step('CreateCampaignPage: set campaign name')
    def set_campaign_name(self, name: str):
        self.campaign_name_input.fill(name)

    @allure.step('CreateCampaignPage: select content')
    def select_content(self):
        self.select_education_contents_button.click()
        return ContentSelectionPage(self.page)

    @allure.step('CreateCampaignPage: create campaign')
    def create_campaign(self):
        self.select_targets()
        self.create_button.click()
        self.ensure_alert_message_is_visible(created_education_campaign_text)


class SpecificEmployees:
    def __init__(self, locator: Locator):
        self.check_box = locator.locator('[data-field="__check__"] input')
        self.first_name = locator.locator('[data-field="first_name"]')
        self.last_name = locator.locator('[data-field="last_name"]')
        self.email = locator.locator('[data-field="email"]')
        self.language = locator.locator('[data-field="language"]')
