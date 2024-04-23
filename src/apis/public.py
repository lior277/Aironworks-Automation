from playwright.sync_api import APIRequestContext
from .psapi import PSApi


class PublicService:
    @classmethod
    def verify_url_click(cls, request_context: APIRequestContext, url: str):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.VERIFY_URL_CLICK.value,
            data={"url": url},
        )
