"""Base API client using Playwright."""

from playwright.sync_api import APIRequestContext, APIResponse


class BaseApi:
    """Base class for API clients using Playwright."""

    def __init__(self, api_context: APIRequestContext):
        self._api = api_context

    def _get(self, url: str, params: dict = None) -> APIResponse:
        response = self._api.get(url, params=params)
        return response

    def _post(self, url: str, data: dict = None) -> APIResponse:
        response = self._api.post(url, data=data)
        return response

    def _put(self, url: str, data: dict = None) -> APIResponse:
        response = self._api.put(url, data=data)
        return response

    def _patch(self, url: str, data: dict = None) -> APIResponse:
        response = self._api.patch(url, data=data)
        return response

    def _delete(self, url: str) -> APIResponse:
        response = self._api.delete(url)
        return response

    def _post_multipart(self, url: str, multipart: dict) -> APIResponse:
        """
        Multipart form upload.

        multipart = {
            "file": {
                "name": "file.csv",
                "mimeType": "text/csv",
                "buffer": file_bytes,
            },
            "field1": "value1",
        }
        """
        response = self._api.post(url, multipart=multipart)
        return response
