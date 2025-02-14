from playwright.sync_api import Locator, Page

from src.page_objects.base_page import BasePage
from src.page_objects.employee_dashboard.completed_education_campaigns_page import (
    CompletedEducationCampaignsPage,
)
from src.page_objects.employee_dashboard.previous_phishing_simulations_page import (
    PreviousPhishingSimulationsPage,
)
from src.page_objects.employee_dashboard.report_history_details_page import (
    ReportHistoryDetailsPage,
)


class EmployeeDashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.greeting_text = self.page.locator('//p[contains(@class,"css-q07viv")]')
        self.level_section = LevelSection(self.page.get_by_label('levelStatus'))
        self.achievements_section = AchievementsSection(
            self.page.get_by_label('achievements')
        )
        self.previous_phishing_simulations_section = PreviousPhishingSimulationsSection(
            self.page.get_by_label('previousPhishingSimulations')
        )
        self.completed_education_campaigns_section = CompletedEducationCampaignsSection(
            self.page.get_by_label('completedEducationCampaigns')
        )
        self.report_history_section = ReportHistorySection(
            self.page.get_by_label('reportHistory')
        )

    def wait_for_page_loaded(self):
        self.greeting_text.wait_for(state='visible')
        components = [
            (self.level_section, 'Level section'),
            (self.achievements_section, 'Achievements section'),
            (
                self.previous_phishing_simulations_section,
                'Previous phishing simulations section',
            ),
            (
                self.completed_education_campaigns_section,
                'Completed education campaigns section',
            ),
            (self.report_history_section, 'Report history section'),
        ]

        for component, name in components:
            component.locator.wait_for(state='visible')
            assert component.locator.is_visible(), f'{name} is NOT visible'

        self.previous_phishing_simulations_section.wait_for_loaded()
        self.completed_education_campaigns_section.wait_for_loaded()
        self.report_history_section.wait_for_loaded()

    def get_greeting_text(self) -> str:
        return self.greeting_text.inner_text()

    def go_to_details(self, section_name: str):
        match section_name:
            case 'Previous Phishing Simulations':
                self.previous_phishing_simulations_section.view_details_button.click()
                return PreviousPhishingSimulationsPage(self.page)
            case 'Completed Education Campaigns':
                self.completed_education_campaigns_section.view_details_button.click()
                return CompletedEducationCampaignsPage(self.page)
            case 'Report History':
                self.report_history_section.view_details_button.click()
                return ReportHistoryDetailsPage(self.page)
            case _:
                raise ValueError(f'Unknown section name: {section_name}')
        return None


class LevelSection:
    def __init__(self, locator: Locator):
        self.locator = locator


class AchievementsSection:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('//p[contains(@class,"css-tswwb7")]')


class PreviousPhishingSimulationsSection:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('//p[contains(@class,"css-tswwb7")]')
        self.view_details_button = self.locator.get_by_role('link', name='View Details')
        self.score_board = self.locator.get_by_label('score')
        self.links_clicked = self.locator.get_by_label('LINKS CLICKED')
        self.emails_opened = self.locator.get_by_label('EMAILS OPENED')
        self.emails_reported_as_suspicion = self.locator.get_by_label(
            'EMAILS REPORTED AS SUSPICION'
        )
        self.emails_reported_as_incident = self.locator.get_by_label(
            'EMAILS REPORTED AS INCIDENT'
        )

    def wait_for_loaded(self):
        components = [
            (self.title, 'Title'),
            (self.view_details_button, 'View details button'),
            (self.score_board, 'Score board'),
            (self.links_clicked, 'Links clicked'),
            (self.emails_opened, 'Emails opened'),
            (self.emails_reported_as_suspicion, 'Emails reported as suspicion'),
            (self.emails_reported_as_incident, 'Emails reported as incident'),
        ]
        for component, name in components:
            component.wait_for(state='visible')
            assert component.is_visible(), f'{name} is NOT visible'


class CompletedEducationCampaignsSection:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('//p[contains(@class,"css-tswwb7")]')
        self.view_details_button = self.locator.get_by_role('link', name='View Details')
        self.campaigns_link = self.locator.get_by_label(
            'Link to education campaign'
        ).nth(0)

    def wait_for_loaded(self):
        components = [
            (self.title, 'Title'),
            (self.view_details_button, 'View details button'),
            (self.campaigns_link, 'Campaigns link'),
        ]
        for component, name in components:
            component.wait_for(state='visible')
            assert component.is_visible(), f'{name} is NOT visible'


class ReportHistorySection:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.title = self.locator.locator('//p[contains(@class,"css-tswwb7")]')
        self.view_details_button = self.locator.get_by_role('link', name='View Details')
        self.all_time_reports = self.locator.get_by_label('All Time')
        self.this_month_reports = self.locator.get_by_label('This Month')
        self.first_report_assessment = self.locator.locator(
            '//div[contains(@class,"css-f10yg6")]'
        ).nth(0)

    def wait_for_loaded(self):
        components = [
            (self.title, 'Title'),
            (self.view_details_button, 'View details button'),
            (self.all_time_reports, 'All time reports'),
            (self.this_month_reports, 'This month reports'),
            (self.first_report_assessment, 'First report assessment'),
        ]
        for component, name in components:
            component.wait_for(state='visible')
            assert component.is_visible(), f'{name} is NOT visible'

    def check_data(self, report_type, status):
        assert self.first_report_assessment.locator(
            f'//p[contains(text(), "{report_type}")]'
        )
        assert self.first_report_assessment.locator(
            f'span[contains(text(), "{status}")]'
        )
