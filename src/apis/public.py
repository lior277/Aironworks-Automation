import allure
from playwright.sync_api import APIRequestContext

from .base_service import BaseService
from .psapi import PSApi


class PublicService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step("EducationService: Simulate user click on sent link {url}")
    def verify_url_click(self, url: str):
        return self._post(PSApi.API_VERSION.value + PSApi.VERIFY_URL_CLICK.value, data={"url": url})
