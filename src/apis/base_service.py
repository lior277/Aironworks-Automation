import json
from functools import wraps

import allure
from playwright.sync_api import APIRequestContext, APIResponse


def allure_attach(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'multipart' in kwargs and kwargs['multipart']:
            allure.attach(
                body=str(kwargs),
                attachment_type=allure.attachment_type.TEXT,
                name='request.text',
            )
        else:
            allure.attach(
                body=json.dumps(kwargs, indent=4),
                attachment_type=allure.attachment_type.JSON,
                name='request.json',
            )

        result = func(*args, **kwargs)
        if result.body():
            if '<html' in result.text():
                allure.attach(
                    body=result.text(),
                    attachment_type=allure.attachment_type.HTML,
                    name='response.html',
                )
            elif result.json():
                allure.attach(
                    body=json.dumps(result.json(), indent=4),
                    attachment_type=allure.attachment_type.JSON,
                    name='response.json',
                )
            else:
                allure.attach(
                    body=result.text(),
                    attachment_type=allure.attachment_type.TEXT,
                    name='response.txt',
                )
        return result

    return wrapper


class BaseService:
    def __init__(self, request_context: APIRequestContext):
        self._request = request_context
        self._request.on('response', allure_attach)

    def _post(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        return self.__request(
            method='POST',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
            multipart=multipart,
        )

    def _get(self, url, data=None, params=None, timeout=None) -> APIResponse:
        return self.__request(
            method='GET', url_or_request=url, data=data, params=params, timeout=timeout
        )

    def _patch(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        return self.__request(
            method='PATCH',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
            multipart=multipart,
        )

    def _delete(self, url, data=None, params=None, timeout=None) -> APIResponse:
        return self.__request(
            method='DELETE',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
        )

    @allure_attach
    def __request(self, **kwargs) -> APIResponse:
        response = self._request.fetch(**kwargs)
        return response
