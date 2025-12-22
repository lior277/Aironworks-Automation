from time import sleep

import allure
from playwright.sync_api import Locator, Page, expect

import src.utils.text_convert as text_convert
from src.models.phish_detect_ui_settings.outlook_localized_config import (
    OutlookConfigData,
)
from src.page_objects.data_types.drop_down_element import DropDown
from src.page_objects.phish_detect_ai_settings.const import updated_settings_text
from src.page_objects.phish_detect_ai_settings.phish_detect_ai_settings_page import (
    PhishDetectAISettings,
)


class PhishDetectAISettingsConfiguration(PhishDetectAISettings):
    def __init__(self, page: Page):
        super().__init__(page)

        self.language_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Language'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.show_preview_button_email_sub_text = self.page.locator(
            "//div[@data-testid='phisshing-assessment-configuration-subTextBlock']/.."
        ).get_by_role('button', name='Show Preview')
        self.show_preview_button_email_waiting_page = self.page.locator(
            "//div[@data-testid='waitingPageConfiguration']/.."
        ).get_by_role('button', name='Show Preview')
        self.show_preview_button_email_phishing_report = self.page.locator(
            "//div[@data-testid='phishing-assessment-configuration-completionReportCustomizationBlock']/.."
        ).get_by_role('button', name='Show Preview')
        self.show_preview_button_email_real_report = self.page.locator(
            "//div[@data-testid='phishing-assessment-configuration-completionRealReportCustomizationBlock']/.."
        ).get_by_role('button', name='Show Preview')
        self.button_visibility_component = ButtonVisibilityComponent(
            self.page.locator("//p[text()='Email Extension UI Configuration']/../../..")
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
            self.page.locator("//p[text()='Assessment Report Preview']/../../..")
        )
        self.platform_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Platform'),
            option_list_locator=self.page.locator('[role="option"]'),
        )

    @allure.step('PhishDetectAISettingsConfiguration: change settings')
    def change_settings(self, settings: OutlookConfigData):
        language_text = text_convert.convert_language_code_to_text(settings.language)
        print('language_text:', language_text)
        self.language_dropdown.select_item_by_text(language_text)
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
            self.show_preview_button_email_sub_text.click()
            self.assessment_preview_window.locator.wait_for()
            sleep(2)

    @allure.step('PhishDetectAISettingsConfiguration: check settings in preview window')
    def check_settings_in_preview(self, settings: OutlookConfigData):
        self.check_settings(settings)
        self.platform_dropdown.select_item_by_text('Gmail')
        self.check_settings(settings)

    @allure.step('PhishDetectAISettingsConfiguration: check settings')
    def check_settings(self, settings: OutlookConfigData):
        self.open_preview_window()
        if settings.assessment_button:
            expect(
                self.assessment_preview_window.get_button(
                    settings.assessment_button_text
                )
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_button_description(
                    settings.assessment_button_description
                )
            ).to_be_visible()

        else:
            expect(
                self.assessment_preview_window.get_button(
                    settings.assessment_button_text
                )
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_button_description(
                    settings.assessment_button_description
                )
            ).not_to_be_visible()

        if settings.incident_button:
            expect(
                self.assessment_preview_window.get_button(settings.incident_button_text)
            ).to_be_visible()
            expect(
                self.assessment_preview_window.get_button_description(
                    settings.incident_button_description
                )
            ).to_be_visible()
        else:
            expect(
                self.assessment_preview_window.get_button(settings.incident_button_text)
            ).not_to_be_visible()
            expect(
                self.assessment_preview_window.get_button_description(
                    settings.incident_button_description
                )
            ).not_to_be_visible()
        self.page.keyboard.press('Escape')


class ButtonVisibilityComponent:
    def __init__(self, locator: Locator):
        self.locator = locator
        self.perform_assessment_enabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-performAssessmentButton"]'
        ).get_by_role('button', name='Enabled')
        self.perform_assessment_disabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-performAssessmentButton"]'
        ).get_by_role('button', name='Disabled')
        self.assessment_button_text_input = self.locator.locator(
            '[id="assessment_button_text-label"]'
        )
        self.assessment_button_description_input = self.locator.locator(
            '[id="assessment_button_description"]'
        )

        self.report_incident_enabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-reportIncidentButton"]'
        ).get_by_role('button', name='Enabled')
        self.report_incident_disabled_button = self.locator.locator(
            '[data-testid="phisshing-assessment-configuration-reportIncidentButton"]'
        ).get_by_role('button', name='Disabled')
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

    @allure.step('AssessmentPreview: get button')
    def get_button(self, button_text: str):
        return self.locator.get_by_role('button', name=button_text)

    @allure.step('AssessmentPreview: get description')
    def get_button_description(self, button_description: str):
        return self.locator.locator(f'//p[contains(text(),"{button_description}")]')
