import json

import allure
from playwright.sync_api import APIRequestContext, APIResponse


def allure_attach(response: APIResponse):
    if response.body():
        if '<html' in response.text():
            allure.attach(
                body=response.text(),
                attachment_type=allure.attachment_type.HTML,
                name='response.html',
            )
        elif response.json():
            allure.attach(
                body=json.dumps(response.json(), indent=4),
                attachment_type=allure.attachment_type.JSON,
                name='response.json',
            )
        else:
            allure.attach(
                body=response.text(),
                attachment_type=allure.attachment_type.TEXT,
                name='response.txt',
            )


class BaseService:
    def __init__(self, request_context: APIRequestContext):
        self._request = request_context
        self._request.on('response', allure_attach)

    def _post(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        response = self._request.post(
            url=url, data=data, params=params, timeout=timeout, multipart=multipart
        )
        allure_attach(response)
        return response

    def _get(self, url, data=None, params=None, timeout=None) -> APIResponse:
        response = self._request.get(url=url, data=data, params=params, timeout=timeout)
        allure_attach(response)
        return response

    def _patch(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        response = self._request.patch(
            url=url, data=data, params=params, timeout=timeout, multipart=multipart
        )
        allure_attach(response)
        return response

    def _delete(self, url, data=None, params=None, timeout=None) -> APIResponse:
        response = self._request.delete(
            url=url, data=data, params=params, timeout=timeout
        )
        allure_attach(response)
        return response
