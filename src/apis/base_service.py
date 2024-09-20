import json
import logging
from functools import wraps

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from .psapi import PSApi

LOGGER = logging.getLogger(__name__)


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

    def _refresh_token(self):
        response = self.__request_with_retry(
            method='POST', url_or_request=PSApi.REFRESH_TOKEN.get_endpoint()
        )
        if response.status != 200:
            raise Exception('Failed to refresh token')

    def _post(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        return self.__request_with_retry(
            method='POST',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
            multipart=multipart,
        )

    def _get(self, url, data=None, params=None, timeout=None) -> APIResponse:
        return self.__request_with_retry(
            method='GET', url_or_request=url, data=data, params=params, timeout=timeout
        )

    def _patch(
        self, url, data=None, params=None, timeout=None, multipart=None
    ) -> APIResponse:
        return self.__request_with_retry(
            method='PATCH',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
            multipart=multipart,
        )

    def _delete(self, url, data=None, params=None, timeout=None) -> APIResponse:
        return self.__request_with_retry(
            method='DELETE',
            url_or_request=url,
            data=data,
            params=params,
            timeout=timeout,
        )

    def __request_with_retry(self, **kwargs) -> APIResponse:
        response = self.__request(**kwargs)
        if response.status == 401:
            self._refresh_token()
            response = self.__request(**kwargs)
        return response

    @allure_attach
    def __request(self, **kwargs) -> APIResponse:
        response = self._request.fetch(**kwargs)
        return response
