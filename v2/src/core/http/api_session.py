import json
import logging
from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config
from v2.src.core.http.retry import retry

LOGGER = logging.getLogger(__name__)


class ApiRequestError(RuntimeError):
    pass


class ApiSession:
    def __init__(self, playwright, storage_state: str):
        self._playwright = playwright
        self._storage_state = storage_state
        self._context: APIRequestContext = self._new_context()

    # ------------------------
    # Context management
    # ------------------------

    def _new_context(self) -> APIRequestContext:
        return self._playwright.request.new_context(
            base_url=Config.BASE_URL, storage_state=self._storage_state
        )

    def close(self):
        self._context.dispose()

    # ------------------------
    # Public API
    # ------------------------

    def get(self, url: str, **kwargs) -> APIResponse:
        return self._request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> APIResponse:
        return self._request('POST', url, **kwargs)

    def patch(self, url: str, **kwargs) -> APIResponse:
        return self._request('PATCH', url, **kwargs)

    def delete(self, url: str, **kwargs) -> APIResponse:
        return self._request('DELETE', url, **kwargs)

    # ------------------------
    # Core request logic
    # ------------------------

    @retry(times=2, exceptions=(ApiRequestError,))
    def _request(self, method: str, url: str, **kwargs) -> APIResponse:
        with allure.step(f'{method} {url}'):
            self._attach_request(method, url, **kwargs)

            response = self._context.fetch(method=method, url=url, **kwargs)

            # Handle auth expiration
            if response.status == 401:
                allure.attach(
                    response.text(),
                    name='401_response.txt',
                    attachment_type=allure.attachment_type.TEXT,
                )
                self._refresh_token()
                response = self._context.fetch(method=method, url=url, **kwargs)

            self._attach_response(response)

            if response.status >= 400:
                raise ApiRequestError(
                    f'{method} {url} failed: {response.status}\n{response.text()}'
                )

            return response

    # ------------------------
    # Token refresh
    # ------------------------

    def _refresh_token(self) -> None:
        with allure.step('Refresh API token'):
            resp = self._context.post(AuthRoutes.REFRESH_TOKEN)
            if not resp.ok:
                raise ApiRequestError(
                    f'Token refresh failed: {resp.status} {resp.text()}'
                )

            # Recreate context to reload cookies
            self._context.dispose()
            self._context = self._new_context()

    # ------------------------
    # Allure helpers
    # ------------------------

    def _attach_request(self, method: str, url: str, **kwargs: Any) -> None:
        payload = {'method': method, 'url': url, 'kwargs': kwargs}
        allure.attach(
            json.dumps(payload, indent=2, default=str),
            name='request.json',
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(self, response: APIResponse) -> None:
        try:
            content = response.json()
            allure.attach(
                json.dumps(content, indent=2),
                name='response.json',
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            allure.attach(
                response.text(),
                name='response.txt',
                attachment_type=allure.attachment_type.TEXT,
            )
