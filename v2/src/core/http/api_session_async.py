import httpx
from typing import Optional

from core.config import Config
from core.exceptions import ApiRequestException, RequestContext


class AsyncApiSession:
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or Config.BASE_URL).rstrip("/")
        self.timeout = timeout or Config.DEFAULT_TIMEOUT

        headers = {
            "User-Agent": "Automation/1.0",
            "Accept": "application/json",
        }

        if Config.API_KEY:
            headers["Authorization"] = f"Bearer {Config.API_KEY}"

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=self.timeout,
            verify=False,
        )

    async def get(self, url: str): return await self._request("GET", url)
    async def post(self, url: str, json_body=None): return await self._request("POST", url, json_body)
    async def put(self, url: str, json_body=None): return await self._request("PUT", url, json_body)
    async def patch(self, url: str, json_body=None): return await self._request("PATCH", url, json_body)
    async def delete(self, url: str, json_body=None): return await self._request("DELETE", url, json_body)

    async def _request(self, method: str, url: str, json_body=None):
        ctx = RequestContext(method=method, url=f"{self.base_url}{url}", body=json_body)

        try:
            response = await self.client.request(method, url, json=json_body)
        except httpx.RequestError as e:
            raise ConnectionError(f"{method} {url} failed: {e}") from e

        if 200 <= response.status_code < 300:
            return response

        ctx.status_code = response.status_code
        ctx.response_text = response.text
        ctx.response_headers = dict(response.headers)
        raise ApiRequestException(ctx)

    async def close(self):
        await self.client.aclose()
