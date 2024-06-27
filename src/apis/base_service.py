import json

import allure
from playwright.sync_api import APIRequestContext, APIResponse


def allure_attach(response: APIResponse):
    allure.attach(
        body=json.dumps(response.json(), indent=4),
        attachment_type=allure.attachment_type.JSON,
        name="response",
    )


class BaseService:
    def __init__(self, request_context: APIRequestContext):
        self._request = request_context
        self._request.on("response", allure_attach)

    def _post(self, url, data=None, params=None, timeout=None) -> APIResponse:
        response = self._request.post(
            url=url, data=data, params=params, timeout=timeout
        )
        allure_attach(response)
        return response

    def _get(self, url, data=None, params=None, timeout=None) -> APIResponse:
        response = self._request.get(url=url, data=data, params=params, timeout=timeout)
        allure_attach(response)
        return response
