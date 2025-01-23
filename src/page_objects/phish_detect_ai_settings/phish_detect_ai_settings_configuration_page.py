import allure
from playwright.sync_api import Locator, Page, expect

from src.models.phish_detect_ui_settings.outlook_localized_config import (
    OutlookConfigData,
)
from src.page_objects.phish_detect_ai_settings.const import updated_settings_text
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_page import (
    PhishDetectAISettings,
)


class PhishDetectAISettingsConfiguration(PhishDetectAISettings):
    def __init__(self, page: Page):
        super().__init__(page)
        self.show_preview_button = self.page.get_by_role('button', name='Show Preview')
        self.button_visibility_component = ButtonVisibilityComponent(
            self.page.locator("//p[text()='Button Visibility']/../..")
        )
        self.completion_report_custom_text_component = (
            CompletionReportCustomTextComponent(
                self.page.locator("//p[text()='Completion Report Custom Text']/../..")
            )
        )
        self.save_component = SaveComponent(
            self.page.locator(
                "//p[text()='Save changes to update PhishDetectAI UI']/../.."
            )
        )
        self.assessment_preview_window = AssessmentPreview(
            self.page.locator(
                "//p[text()='PhishDectectAI Assessment Preview']/../../.."
            )
        )

    @allure.step('PhishDetectAISettingsConfiguration: change settings')
    def change_settings(self, settings: OutlookConfigData):
        if settings.assessment_button:
            self.button_visibility_component.perform_assessment_enabled_button.click()
        else:
            self.button_visibility_component.perform_assessment_disabled_button.click()
        if settings.incident_button:
            self.button_visibility_component.report_incident_enabled_button.click()
        else:
            self.button_visibility_component.report_incident_disabled_button.click()
        if settings.completion_report_custom_text:
            self.completion_report_custom_text_component.custom_text_input.fill(
                settings.completion_report_custom_text
            )

        self.save_component.save_button.click()
        self.ensure_alert_message_is_visible(updated_settings_text)

    @allure.step('PhishDetectAISettingsConfiguration: open preview window')
    def open_preview_window(self):
        if not self.assessment_preview_window.locator.is_visible():
            self.show_preview_button.click()
            self.assessment_preview_window.locator.wait_for()

    @allure.step('PhishDetectAISettingsConfiguration: check settings in preview window')
    def check_settings_in_preview(self, settings: OutlookConfigData):
        self.open_preview_window()
        if settings.assessment_button:
            expect(
                self.assessment_preview_window.get_outlook_button(
                    settings.assessment_button_text
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_outlook_button_description(
                    settings.assessment_button_description
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button(
                    settings.assessment_button_text
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button_description(
                    settings.assessment_button_description
                )
            ).to_be_visible()
        else:
            expect(
                self.assessment_preview_window.get_outlook_button(
                    settings.assessment_button_text
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_outlook_button_description(
                    settings.assessment_button_description
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button(
                    settings.assessment_button_text
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button_description(
                    settings.assessment_button_description
                )
            ).not_to_be_visible()

        if settings.incident_button:
            expect(
                self.assessment_preview_window.get_outlook_button(
                    settings.incident_button_text
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_outlook_button_description(
                    settings.incident_button_description
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button(
                    settings.incident_button_text
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button_description(
                    settings.incident_button_description
                )
            ).to_be_visible()
        else:
            expect(
                self.assessment_preview_window.get_outlook_button(
                    settings.incident_button_text
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_outlook_button_description(
                    settings.incident_button_description
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button(
                    settings.incident_button_text
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_gmail_button_description(
                    settings.incident_button_description
                )
            ).not_to_be_visible()


class ButtonVisibilityComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.perform_assessment_enabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-performAssessmentButton"]'
        ).get_by_label('Enabled')
        self.perform_assessment_disabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-performAssessmentButton"]'
        ).get_by_label('Disabled')
        self.assessment_button_text_input = self.locator.locator(
            '[id="assessment_button_text-label"]'
        )
        self.assessment_button_description_input = self.locator.locator(
            '[id="assessment_button_description"]'
        )

        self.report_incident_enabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-reportIncidentButton"]'
        ).get_by_label('Enabled')
        self.report_incident_disabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-reportIncidentButton"]'
        ).get_by_label('Disabled')
        self.incident_button_text_input = self.locator.locator(
            '[id="incident_button_text-label"]'
        )
        self.incident_button_description_input = self.locator.locator(
            '[id="incident_button_description"]'
        )

        self.sub_text_input = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-subTextBlock"] #subtext'
        )


class CompletionReportCustomTextComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.custom_text_input = self.locator.get_by_role('textbox', name='Custom text')


class SaveComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.discard_button = self.locator.get_by_role('button', name='Discard')
        self.save_button = self.locator.get_by_role('button', name='Save')


class AssessmentPreview:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.outlook_section = self.locator.locator(
            "//p[contains(text(),'Outlook')]/.."
        )
        self.gmail_section = self.locator.locator("//p[contains(text(),'Gmail')]/..")

    @allure.step('AssessmentPreview: get outlook button')
    def get_outlook_button(self, button_text: str):
        return self.outlook_section.get_by_role('button', name=button_text)

    @allure.step('AssessmentPreview: get outlook description')
    def get_outlook_button_description(self, button_description: str):
        return self.outlook_section.locator(
            f'//p[contains(text(),"{button_description}")]'
        )

    @allure.step('AssessmentPreview: get gmail button')
    def get_gmail_button(self, button_text: str):
        return self.gmail_section.get_by_role('button', name=button_text)

    @allure.step('AssessmentPreview: get gmail description')
    def get_gmail_button_description(self, button_description: str):
        return self.gmail_section.locator(
            f'//p[contains(text(),"{button_description}")]'
        )
