from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING, Any
from urllib.parse import urlencode

from playwright.sync_api import APIRequestContext, APIResponse, Playwright

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config

if TYPE_CHECKING:
    from playwright.sync_api import StorageState

LOGGER = logging.getLogger(__name__)

HTTP_ERROR_THRESHOLD = 400
REDACT_HEADER_KEYS = ('authorization', 'cookie', 'set-cookie')


def _redact_headers(headers: dict[str, Any] | None) -> dict[str, Any] | None:
    if not headers:
        return headers
    out = dict(headers)
    for k in list(out.keys()):
        if k.lower() in REDACT_HEADER_KEYS:
            out[k] = '***REDACTED***'
    return out


class ApiRequestError(RuntimeError):
    def __init__(
        self,
        *,
        method: str,
        url: str,
        status: int,
        request_headers: dict[str, Any] | None = None,
        response_headers: dict[str, Any] | None = None,
        response_text: str | None = None,
    ):
        parts = ['API REQUEST FAILED', f'{method} {url}', f'Status: {status}']
        if request_headers:
            parts.append(
                'Request headers:\n'
                + json.dumps(_redact_headers(request_headers), indent=2, default=str)
            )
        if response_headers:
            parts.append(
                'Response headers:\n'
                + json.dumps(_redact_headers(response_headers), indent=2, default=str)
            )
        if response_text:
            parts.append('Response body:\n' + response_text)

        super().__init__('\n' + '\n'.join(parts) + '\n')
        self.status = status
        self.method = method
        self.url = url
        self.response_text = response_text


class ApiSession:
    """Playwright APIRequestContext wrapper. One session per worker."""

    def __init__(
        self,
        playwright: Playwright,
        *,
        base_url: str,
        storage_state: str | None = None,
        enable_refresh: bool = True,
        default_headers: dict[str, str] | None = None,
        retries: int | None = None,
        retry_on_status: set[int] | None = None,
        retry_delay_sec: float | None = None,
    ):
        self._playwright = playwright
        self._base_url = base_url.rstrip('/')
        self._storage_state = storage_state
        self._enable_refresh = enable_refresh
        self._default_headers = default_headers or {}

        # per-session overrides (Mailtrap can use different retry policy)
        self._retries = Config.API_RETRIES if retries is None else int(retries)
        self._retry_on_status = (
            set(Config.API_RETRY_ON_STATUS)
            if retry_on_status is None
            else set(retry_on_status)
        )
        self._retry_delay_sec = (
            Config.API_RETRY_DELAY_SEC
            if retry_delay_sec is None
            else float(retry_delay_sec)
        )

        self._closed = False
        self._context: APIRequestContext = self._create_context()

    def get(self, url: str, **kwargs) -> APIResponse:
        return self._request('GET', url, **kwargs)

    def post(self, url: str, **kwargs) -> APIResponse:
        return self._request('POST', url, **kwargs)

    def patch(self, url: str, **kwargs) -> APIResponse:
        return self._request('PATCH', url, **kwargs)

    def delete(self, url: str, **kwargs) -> APIResponse:
        return self._request('DELETE', url, **kwargs)

    def close(self) -> None:
        if self._closed:
            return
        try:
            self._context.dispose()
        finally:
            self._closed = True

    def storage_state(self) -> 'StorageState':
        return self._context.storage_state()

    def save_storage_state(self, path: Any) -> None:
        self._context.storage_state(path=str(path))

    def _create_context(self) -> APIRequestContext:
        if not self._base_url:
            raise RuntimeError('base_url is empty')

        kwargs: dict[str, Any] = {'base_url': self._base_url}

        if self._storage_state:
            kwargs['storage_state'] = self._storage_state

        # Default headers applied to every request (perfect for Mailtrap Api-Token).
        if self._default_headers:
            kwargs['extra_http_headers'] = dict(self._default_headers)

        return self._playwright.request.new_context(**kwargs)

    def _merge_headers(
        self, call_headers: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if not self._default_headers and not call_headers:
            return call_headers

        merged: dict[str, Any] = (
            dict(self._default_headers) if self._default_headers else {}
        )

        if call_headers:
            # override defaults case-insensitively
            for k, v in call_headers.items():
                for existing in list(merged.keys()):
                    if existing.lower() == k.lower():
                        merged.pop(existing)
                        break
                merged[k] = v

        return merged

    def _normalize_payload(self, kwargs: dict[str, Any]) -> dict[str, Any]:
        if 'json' not in kwargs:
            return kwargs

        normalized = dict(kwargs)
        payload = normalized.pop('json')
        normalized['data'] = json.dumps(payload)

        headers = dict(normalized.get('headers') or {})
        if not any(k.lower() == 'content-type' for k in headers):
            headers['content-type'] = 'application/json'
        normalized['headers'] = headers
        return normalized

    @staticmethod
    def _apply_params(url: str, params: dict[str, Any] | None) -> str:
        if not params:
            return url
        q = urlencode(params, doseq=True)
        return f'{url}{"&" if "?" in url else "?"}{q}'

    def _should_retry(self, status: int, attempt: int, max_attempts: int) -> bool:
        return status in self._retry_on_status and attempt < max_attempts

    def _should_attempt_refresh(self, url: str, status: int, did_refresh: bool) -> bool:
        if not (self._enable_refresh and (not did_refresh) and status == 401):
            return False

        blocked = (AuthRoutes.LOGIN, AuthRoutes.REFRESH_TOKEN, AuthRoutes.LOGOUT)
        return not any(url.startswith(p) for p in blocked)

    def _refresh(self) -> bool:
        resp = self._context.fetch(
            AuthRoutes.REFRESH_TOKEN,
            method='POST',
            headers=self._merge_headers(None),
            timeout=Config.DEFAULT_TIMEOUT_SEC * 1000,
        )
        return resp.status < HTTP_ERROR_THRESHOLD

    @staticmethod
    def _safe_text(response: APIResponse) -> str | None:
        try:
            return response.text()
        except Exception:
            return None

    @staticmethod
    def _safe_headers(response: APIResponse) -> dict[str, Any] | None:
        try:
            return dict(response.headers)
        except Exception:
            return None

    def _raise_for_status(
        self,
        *,
        method: str,
        url: str,
        response: APIResponse,
        request_headers: dict[str, Any] | None,
    ) -> None:
        if response.status < HTTP_ERROR_THRESHOLD:
            return
        raise ApiRequestError(
            method=method,
            url=url,
            status=response.status,
            request_headers=request_headers,
            response_headers=self._safe_headers(response),
            response_text=self._safe_text(response),
        )

    def _fetch_once(
        self, method: str, url: str, kwargs: dict[str, Any]
    ) -> tuple[str, APIResponse, dict[str, Any] | None]:
        call_kwargs = dict(kwargs)

        merged_headers = self._merge_headers(call_kwargs.get('headers'))
        call_kwargs['headers'] = merged_headers

        call_kwargs = self._normalize_payload(call_kwargs)
        call_kwargs.setdefault('timeout', Config.DEFAULT_TIMEOUT_SEC * 1000)

        params = call_kwargs.pop('params', None)
        final_url = self._apply_params(url, params)

        response = self._context.fetch(final_url, method=method, **call_kwargs)
        return final_url, response, merged_headers

    def _request(self, method: str, url: str, **kwargs) -> APIResponse:
        max_attempts = self._retries + 1
        did_refresh = False

        for attempt in range(1, max_attempts + 1):
            final_url, response, merged_headers = self._fetch_once(method, url, kwargs)

            if self._should_attempt_refresh(final_url, response.status, did_refresh):
                if self._refresh():
                    did_refresh = True
                    continue

            if self._should_retry(response.status, attempt, max_attempts):
                LOGGER.warning(
                    'Transient error: %s %s status=%s attempt=%s/%s',
                    method,
                    final_url,
                    response.status,
                    attempt,
                    max_attempts,
                )
                time.sleep(self._retry_delay_sec)
                continue

            self._raise_for_status(
                method=method,
                url=final_url,
                response=response,
                request_headers=merged_headers,
            )
            return response

        raise RuntimeError('Request loop exited unexpectedly')
