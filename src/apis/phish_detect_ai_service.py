import dataclasses

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.base_service import BaseService
from src.apis.psapi import PSApi
from src.models.phish_detect_ui_settings.outlook_localized_config import (
    OutlookConfigData,
)


class PhishDetectUI(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('PhishDetectUI: get outlook localized config')
    def get_outlook_localized_config(self) -> APIResponse:
        return self._get(PSApi.OUTLOOK_LOCALIZED_CONFIG.get_endpoint())

    @allure.step(
        'PhishDetectUI: update outlook localized config for {language} language'
    )
    def update_outlook_localized_config(
        self, data: OutlookConfigData, language: str = 'en'
    ):
        updated_data = dataclasses.replace(data)
        updated_data.language = None
        updated_data = updated_data.to_filtered_dict()

        return self._patch(
            PSApi.OUTLOOK_LOCALIZED_CONFIG_LANGUAGE.get_endpoint().format(
                language=language
            ),
            data=updated_data,
        )
