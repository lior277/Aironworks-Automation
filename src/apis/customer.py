import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.psapi import PSApi


class CustomerService:
    @classmethod
    @allure.step("CustomerService: get customer attack page preview")
    def get_customer_attack_page_preview(cls, request_context: APIRequestContext) -> APIResponse:
        return request_context.post(PSApi.CUSTOMER_ATTACK_PAGE_PREVIEW.get_endpoint())
