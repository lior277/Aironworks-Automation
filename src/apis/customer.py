import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.base_service import BaseService
from src.apis.psapi import PSApi


class CustomerService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step("CustomerService: get customer attack page preview")
    def get_customer_attack_page_preview(self) -> APIResponse:
        return self._post(PSApi.CUSTOMER_ATTACK_PAGE_PREVIEW.get_endpoint())
