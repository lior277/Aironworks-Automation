from playwright.sync_api import APIRequestContext
from .psapi import PSApi
import allure


class PublicService:
    @classmethod
    @allure.step("EducationService: Simulate user click on sent link")
    def verify_url_click(cls, request_context: APIRequestContext, url: str):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.VERIFY_URL_CLICK.value,
            data={"url": url},
        )
