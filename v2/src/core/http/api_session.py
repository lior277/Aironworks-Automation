"""
HTTP client for test automation (sync).
"""

import requests
from requests.adapters import HTTPAdapter
from typing import Optional, Any

from v2.src.core.config import Config
from v2.src.core.exceptions import ApiRequestException, RequestContext
from v2.src.core.http.http_utils import create_retry_strategy


# Type aliases
JsonBody = dict | list | None
FormData = dict[str, tuple]  # {"file": ("name.pdf", fileobj_or_bytes, "application/pdf")}


class ApiSession:
    """
    HTTP client with retry logic and authentication.

    Usage:
        session = ApiSession()
        response = session.get(ApiRoutes.get_user_by_id(123))
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        api_key: Optional[str] = None,
    ):
        self.base_url = (base_url or Config.BASE_URL).rstrip("/")
        self.timeout = timeout or Config.DEFAULT_TIMEOUT
        self.api_key = api_key or Config.API_KEY

        self.session = self._create_session()

    # ─────────────────────────────────────────────
    # Session setup
    # ─────────────────────────────────────────────

    def _create_session(self) -> requests.Session:
        session = requests.Session()

        adapter = HTTPAdapter(max_retries=create_retry_strategy())
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update({
            "User-Agent": "Automation/1.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

        if self.api_key:
            session.headers["Authorization"] = f"Bearer {self.api_key}"

        return session

    # ─────────────────────────────────────────────
    # Public HTTP Methods (JSON)
    # ─────────────────────────────────────────────

    def get(self, url: str) -> requests.Response:
        return self._request("GET", url)

    def post(self, url: str, json_body: JsonBody = None) -> requests.Response:
        return self._request("POST", url, json_body)

    def put(self, url: str, json_body: JsonBody = None) -> requests.Response:
        return self._request("PUT", url, json_body)

    def patch(self, url: str, json_body: JsonBody = None) -> requests.Response:
        return self._request("PATCH", url, json_body)

    def delete(self, url: str, json_body: JsonBody = None) -> requests.Response:
        return self._request("DELETE", url, json_body)

    # ─────────────────────────────────────────────
    # Multipart / Form-Data (C# MultipartFormDataContent equivalent)
    # ─────────────────────────────────────────────

    def post_form(
        self,
        url: str,
        files: FormData,
        data: dict | None = None,
    ) -> requests.Response:
        """
        Multipart/form-data POST (file upload, etc).

        files example:
        {
            "file": ("logo.png", open("logo.png", "rb"), "image/png")
        }
        """
        full_url = self._full_url(url)

        request_context = RequestContext(
            method="POST",
            url=full_url,
            body={"files": list(files.keys()), "data": data},
        )

        # Remove Content-Type so requests will set multipart boundary correctly
        headers = {k: v for k, v in self.session.headers.items() if k != "Content-Type"}

        try:
            response = self.session.post(
                full_url,
                files=files,
                data=data,
                headers=headers,
                timeout=self.timeout,
                verify=False,
            )
        except requests.RequestException as e:
            raise ConnectionError(f"Request failed: POST {full_url} - {e}") from e

        self._validate(response, request_context)
        return response

    # ─────────────────────────────────────────────
    # Core request logic
    # ─────────────────────────────────────────────

    def _request(self, method: str, url: str, json_body: JsonBody = None) -> requests.Response:
        full_url = self._full_url(url)

        request_context = RequestContext(
            method=method,
            url=full_url,
            body=json_body,
        )

        try:
            response = self.session.request(
                method=method,
                url=full_url,
                json=json_body,
                timeout=self.timeout,
                verify=False,
            )
        except requests.RequestException as e:
            raise ConnectionError(f"Request failed: {method} {full_url} - {e}") from e

        self._validate(response, request_context)
        return response

    # ─────────────────────────────────────────────
    # Validation
    # ─────────────────────────────────────────────

    def _validate(self, response: requests.Response, request_context: RequestContext) -> None:
        if response.ok:
            return

        request_context.status_code = response.status_code
        request_context.response_text = response.text
        request_context.response_headers = dict(response.headers)

        raise ApiRequestException(request_context)

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────

    def _full_url(self, url: str) -> str:
        if url.startswith("http"):
            return url
        return f"{self.base_url}{url}"
