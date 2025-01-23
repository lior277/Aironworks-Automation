import allure
from playwright.sync_api import Page, expect

from src.page_objects.campaigns_page import CampaignsPage
from src.page_objects.content_library.content_library_page import ContentLibraryPage
from src.page_objects.education_campaign.education_campaign_page import (
    EducationCampaignPage,
)
from src.page_objects.email_filter.email_filter_settings_page import (
    EmailFilterSettingsPage,
)
from src.page_objects.email_filter.email_statistics_page import EmailStatisticsPage
from src.page_objects.email_filter.received_emails_page import ReceivedEmailsPage
from src.page_objects.employee_directory.employee_directory_page import (
    EmployeeDirectoryPage,
)
from src.page_objects.employee_reports_page import EmployeeReportsPage
from src.page_objects.groups.groups_page import GroupsPage
from src.page_objects.phish_detect_ai_settings.const import phishing_assessment_title
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_configuration_page import (
    PhishDetectAISettingsConfiguration,
)
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_general_page import (
    PhishDetectAISettingsGeneral,
)
from src.page_objects.scenarios_page import ScenariosPage
from src.page_objects.training_settings.email_sending_page import EmailSendingPage
from src.page_objects.training_settings.training_settings_page import (
    TrainingSettingsPage,
)


class NavigationBar:
    def __init__(self, page: Page):
        self.page = page
        self.scenarios_button = page.get_by_role('link', name='Scenarios')
        self.training_settings_button = page.get_by_role(
            'link', name='Training Settings', exact=True
        )
        self.employee_reports_button = page.get_by_role(
            'link', name='PhishDetectAI Reports'
        )
        self.content_library_button = page.get_by_role('link', name='Content Library')
        self.campaigns_button = page.get_by_role('link', name='Campaigns', exact=True)
        self.employee_directory_button = page.get_by_role(
            'link', name='Employee directory', exact=True
        )
        self.education_campaigns_button = page.get_by_role(
            'link', name='Education Campaigns', exact=True
        )
        self.groups_button = page.get_by_role('link', name='Groups', exact=True)
        self.phish_detect_ai_settings_button = page.get_by_role(
            'link', name='PhishDetectAI Settings', exact=True
        )
        self.email_statistics_button = page.get_by_role('link', name='Email Statistics')
        self.received_emails_button = page.get_by_role('link', name='Received Emails')
        self.email_filter_settings_button = page.get_by_role(
            'link', name='Email Filter Settings'
        )

    @allure.step('NavigationBar: Navigate to scenarios')
    def navigate_scenarios(self):
        self.scenarios_button.click()
        scenario_page = ScenariosPage(self.page)
        scenario_page.wait_for_progress_bar_disappears()
        return scenario_page

    @allure.step('NavigationBar: Navigate to settings')
    def navigate_settings(self):
        self.settings_button.click()
        self.page.wait_for_load_state(timeout=5)
        return TrainingSettingsPage(self.page)

    @allure.step('NavigationBar: Navigate to employee reports')
    def navigate_employee_reports(self):
        self.employee_reports_button.click()
        self.page.wait_for_load_state(timeout=5)

        return EmployeeReportsPage(self.page)

    @allure.step('NavigationBar: Navigate to content library')
    def navigate_content_library(self):
        self.content_library_button.click()
        content_library_page = ContentLibraryPage(self.page)
        content_library_page.add_content_button.wait_for()
        content_library_page.wait_for_progress_bar_disappears()
        return ContentLibraryPage(self.page)

    @allure.step('NavigationBar: Navigate to campaigns')
    def navigate_campaigns(self):
        self.campaigns_button.click()
        self.page.wait_for_load_state(timeout=5)

        return CampaignsPage(self.page)

    @allure.step('NavigationBar: Navigate to employee directory page')
    def navigate_employee_directory(self) -> EmployeeDirectoryPage:
        self.employee_directory_button.click()
        employee_directory_page = EmployeeDirectoryPage(self.page)
        employee_directory_page.deactivate_button.wait_for()
        employee_directory_page.wait_for_loading_state()
        return employee_directory_page

    @allure.step('NavigationBar: Navigate to education campaigns page')
    def navigate_education_campaigns_page(self):
        self.education_campaigns_button.click()
        education_page = EducationCampaignPage(self.page)
        education_page.title.wait_for()
        education_page.wait_for_loading_state()
        return education_page

    @allure.step('NavigationBar: Navigate to groups page')
    def navigate_groups_page(self) -> GroupsPage:
        self.groups_button.click()
        groups_page = GroupsPage(self.page)
        groups_page.wait_for_progress_bar_disappears()
        return groups_page

    @allure.step('NavigationBar: Navigate to groups page')
    def navigate_phish_detect_ai_settings_general_page(
        self,
    ) -> PhishDetectAISettingsGeneral:
        self.phish_detect_ai_settings_button.click()
        phish_detect_ai_settings_page = PhishDetectAISettingsGeneral(self.page)
        phish_detect_ai_settings_page.email_input.wait_for()
        expect(phish_detect_ai_settings_page.title).to_contain_text(
            phishing_assessment_title
        )
        phish_detect_ai_settings_page.wait_for_progress_bar_disappears()
        return phish_detect_ai_settings_page

    @allure.step('NavigationBar: Navigate to groups page')
    def navigate_phish_detect_ai_settings_ui_page(
        self,
    ) -> PhishDetectAISettingsConfiguration:
        self.navigate_phish_detect_ai_settings_general_page()
        ui_configuration_page = PhishDetectAISettingsConfiguration(self.page)
        ui_configuration_page.ui_configuration_tab.click()
        ui_configuration_page.show_preview_button.wait_for()
        return ui_configuration_page

    @allure.step('NavigationBar: Navigate to email statistics page')
    def navigate_email_statistics_page(self):
        self.email_statistics_button.click()
        email_statistics_page = EmailStatisticsPage(self.page)
        email_statistics_page.wait_for_progress_bar_disappears()
        return email_statistics_page

    @allure.step('NavigationBar: Navigate to received emails page')
    def navigate_received_emails_page(self):
        self.received_emails_button.click()
        received_emails_page = ReceivedEmailsPage(self.page)
        received_emails_page.wait_for_progress_bar_disappears()
        return received_emails_page

    @allure.step('NavigationBar: Navigate to email filter settings page')
    def navigate_email_filter_settings_page(self):
        self.email_filter_settings_button.click()
        email_filter_settings_page = EmailFilterSettingsPage(self.page)
        email_filter_settings_page.wait_for_progress_bar_disappears()
        return email_filter_settings_page

    @allure.step('NavigationBar: Navigate to training settings: email sending page')
    def navigate_training_settings_email_sending_page(self):
        self.training_settings_button.click()
        email_sending_page = EmailSendingPage(self.page)
        email_sending_page.select_tab('Email Sending')
        email_sending_page.wait_for_progress_bar_disappears()
        return email_sending_page
