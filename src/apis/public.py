from enum import Enum
from typing import List
from playwright.sync_api import APIRequestContext


class PublicApi(Enum):
    API_VERSION = "/api"

    VERIFY_URL_CLICK = "/public/verify_url_click"


class PublicService:
    @classmethod
    def verify_url_click(cls, request_context: APIRequestContext, url: str):
        return request_context.post(
            PublicApi.API_VERSION.value + PublicApi.VERIFY_URL_CLICK.value,
            data={"url": url},
        )
