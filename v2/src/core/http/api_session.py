"""
Simplified API session with clean error handling.
Follows SOLID principles - Single Responsibility.
"""

import json
import logging
from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse, Playwright

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config

LOGGER = logging.getLogger(__name__)


class ApiRequestError(RuntimeError):
    """API request failed."""

    pass


class ApiSession:
    """
    Simplified API session with automatic token refresh.
    Single Responsibility: HTTP requests with authentication.
    """

    def __init__(self, playwright: Playwright, storage_state: str):
        self._playwright = playwright
        self._storage_state = storage_state
        self._context: APIRequestContext = self._create_context()

    # ---------------
    # Public API
    # ---------------

    def get(self, url: str, **kwargs) -> APIResponse:
        """GET request."""
        return self._request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> APIResponse:
        """POST request."""
        return self._request('POST', url, **kwargs)

    def patch(self, url: str, **kwargs) -> APIResponse:
        """PATCH request."""
        return self._request('PATCH', url, **kwargs)

    def delete(self, url: str, **kwargs) -> APIResponse:
        """DELETE request."""
        return self._request('DELETE', url, **kwargs)

    def close(self):
        """Close API context."""
        self._context.dispose()

    # ---------------
    # Internal
    # ---------------

    def _create_context(self) -> APIRequestContext:
        """Create new API context with auth."""
        return self._playwright.request.new_context(
            base_url=Config.BASE_URL, storage_state=self._storage_state
        )

    def _request(self, method: str, url: str, **kwargs) -> APIResponse:
        """
        Execute request with automatic retry on 401.
        Clean and simple - no over-engineering.
        """
        with allure.step(f'{method} {url}'):
            # Log request
            self._log_request(method, url, **kwargs)

            # Make request
            response = self._context.fetch(method=method, url=url, **kwargs)

            # Handle 401 - refresh token and retry once
            if response.status == 401:
                with allure.step('Token expired - refreshing'):
                    self._refresh_token()
                    response = self._context.fetch(method=method, url=url, **kwargs)

            # Log response
            self._log_response(response)

            # Check for errors
            if response.status >= 400:
                error_msg = (
                    f'{method} {url} failed: {response.status}\n{response.text()}'
                )
                LOGGER.error(error_msg)
                raise ApiRequestError(error_msg)

            return response

    def _refresh_token(self) -> None:
        """Refresh authentication token."""
        with allure.step('Refreshing API token'):
            resp = self._context.post(AuthRoutes.REFRESH_TOKEN)

            if not resp.ok:
                raise ApiRequestError(
                    f'Token refresh failed: {resp.status} {resp.text()}'
                )

            # Recreate context with fresh cookies
            self._context.dispose()
            self._context = self._create_context()

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        """Log request to Allure."""
        payload = {
            'method': method,
            'url': url,
            'kwargs': {k: v for k, v in kwargs.items() if k != 'data'},
        }

        # Add data if present
        if 'data' in kwargs:
            payload['data'] = kwargs['data']

        allure.attach(
            json.dumps(payload, indent=2, default=str),
            name='request.json',
            attachment_type=allure.attachment_type.JSON,
        )

    def _log_response(self, response: APIResponse) -> None:
        """Log response to Allure."""
        try:
            content = response.json()
            allure.attach(
                json.dumps(content, indent=2),
                name=f'response_{response.status}.json',
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            allure.attach(
                response.text(),
                name=f'response_{response.status}.txt',
                attachment_type=allure.attachment_type.TEXT,
            )
