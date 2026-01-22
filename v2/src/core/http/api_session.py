"""API session built on Playwright request context."""

from __future__ import annotations

import json
from typing import Any

import allure
from playwright.sync_api import APIRequestContext, APIResponse, Playwright

from v2.src.core.config import Config
from v2.src.core.exceptions import ApiRequestException, RequestContext
from v2.src.core.http.retry import RetryPolicy

JsonBody = dict | list | None
Multipart = dict[str, Any] | None


class ApiSession:
    """
    Thin wrapper around Playwright APIRequestContext.

    Features:
    - retries (timeouts/network/5xx)
    - multipart support
    - rich exceptions
    - Allure request/response attachments
    """

    def __init__(
        self,
        playwright: Playwright,
        storage_state_path: str,
        base_url: str | None = None,
        retry_policy: RetryPolicy | None = None,
    ):
        self.base_url = (base_url or Config.BASE_URL).rstrip('/')

        self._ctx: APIRequestContext = playwright.request.new_context(
            base_url=self.base_url, storage_state=storage_state_path
        )

        self._retry = retry_policy or RetryPolicy(
            retries=Config.API_RETRIES,
            delay=Config.API_RETRY_DELAY_SEC,
            retry_on_status=Config.API_RETRY_ON_STATUS,
        )

    # ------------- Public methods -------------

    def get(
        self, url: str, *, params: dict | None = None, timeout_ms: int | None = None
    ) -> APIResponse:
        return self._request('GET', url, params=params, timeout_ms=timeout_ms)

    def post(
        self,
        url: str,
        *,
        json_body: JsonBody = None,
        multipart: Multipart = None,
        params: dict | None = None,
        timeout_ms: int | None = None,
    ) -> APIResponse:
        return self._request(
            'POST',
            url,
            json_body=json_body,
            multipart=multipart,
            params=params,
            timeout_ms=timeout_ms,
        )

    def patch(
        self,
        url: str,
        *,
        json_body: JsonBody = None,
        multipart: Multipart = None,
        params: dict | None = None,
        timeout_ms: int | None = None,
    ) -> APIResponse:
        return self._request(
            'PATCH',
            url,
            json_body=json_body,
            multipart=multipart,
            params=params,
            timeout_ms=timeout_ms,
        )

    def delete(
        self, url: str, *, params: dict | None = None, timeout_ms: int | None = None
    ) -> APIResponse:
        return self._request('DELETE', url, params=params, timeout_ms=timeout_ms)

    def close(self) -> None:
        self._ctx.dispose()

    # ------------- Core request logic -------------

    def _request(
        self,
        method: str,
        url: str,
        *,
        json_body: JsonBody = None,
        multipart: Multipart = None,
        params: dict | None = None,
        timeout_ms: int | None = None,
    ) -> APIResponse:
        def do_call() -> APIResponse:
            return self._request_once(
                method,
                url,
                json_body=json_body,
                multipart=multipart,
                params=params,
                timeout_ms=timeout_ms,
            )

        response = self._retry.run(do_call)

        # Only 401 triggers auth refresh/retry (optional hook)
        if response.status == 401:
            self._refresh_auth()
            response = self._retry.run(do_call)

        return response

    def _request_once(
        self,
        method: str,
        url: str,
        *,
        json_body: JsonBody,
        multipart: Multipart,
        params: dict | None,
        timeout_ms: int | None,
    ) -> APIResponse:
        request_kwargs = {'method': method, 'url': url, 'params': params}

        if timeout_ms is not None:
            request_kwargs['timeout'] = timeout_ms

        # Playwright accepts either `json=` or `multipart=`
        if multipart is not None and json_body is not None:
            raise ValueError('Use either json_body or multipart, not both.')

        if json_body is not None:
            request_kwargs['json'] = json_body

        if multipart is not None:
            request_kwargs['multipart'] = multipart

        self._allure_attach_request(
            method, url, json_body=json_body, multipart=multipart, params=params
        )

        response = self._ctx.fetch(**request_kwargs)

        self._allure_attach_response(response)

        if not response.ok:
            ctx = RequestContext(
                method=method,
                url=self._absolute_url(url),
                body=json_body if json_body is not None else multipart,
                status_code=response.status,
                response_text=response.text(),
                response_headers=dict(response.headers),
            )
            raise ApiRequestException(ctx)

        return response

    def _refresh_auth(self) -> None:
        """
        Optional: implement refresh token flow if your backend supports it.
        If you don't have a refresh endpoint, leave it empty.
        """
        return

    # ------------- Helpers -------------

    def _absolute_url(self, url: str) -> str:
        if url.startswith('http'):
            return url
        return f'{self.base_url}{url}'

    def _allure_attach_request(
        self,
        method: str,
        url: str,
        *,
        json_body: JsonBody,
        multipart: Multipart,
        params: dict | None,
    ) -> None:
        payload = {
            'method': method,
            'url': self._absolute_url(url),
            'params': params,
            'json': json_body,
            'multipart_keys': list(multipart.keys())
            if isinstance(multipart, dict)
            else None,
        }
        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False, default=str),
            name='api.request',
            attachment_type=allure.attachment_type.JSON,
        )

    def _allure_attach_response(self, response: APIResponse) -> None:
        meta = {'status': response.status, 'headers': dict(response.headers)}
        allure.attach(
            json.dumps(meta, indent=2, ensure_ascii=False, default=str),
            name='api.response.meta',
            attachment_type=allure.attachment_type.JSON,
        )

        text = ''
        try:
            text = response.text()
        except Exception:
            return

        if not text:
            return

        # Attach HTML / JSON / text
        if text.lstrip().startswith('<'):
            allure.attach(
                text,
                name='api.response.html',
                attachment_type=allure.attachment_type.HTML,
            )
            return

        try:
            obj = response.json()
            allure.attach(
                json.dumps(obj, indent=2, ensure_ascii=False, default=str),
                name='api.response.json',
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception:
            allure.attach(
                text,
                name='api.response.text',
                attachment_type=allure.attachment_type.TEXT,
            )
