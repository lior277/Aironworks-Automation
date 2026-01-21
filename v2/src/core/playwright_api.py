from playwright.sync_api import APIRequestContext


class PlaywrightApi:

    def __init__(self, api_context: APIRequestContext):
        self.api = api_context

    def get(self, url: str):
        resp = self.api.get(url)
        self._check(resp, "GET", url)
        return resp

    def post(self, url: str, data=None, multipart=None):
        resp = self.api.post(url, data=data, multipart=multipart)
        self._check(resp, "POST", url)
        return resp

    def delete(self, url: str):
        resp = self.api.delete(url)
        self._check(resp, "DELETE", url)
        return resp

    def _check(self, resp, method, url):
        if not resp.ok:
            raise Exception(
                f"API ERROR {method} {url}\n"
                f"Status: {resp.status}\n"
                f"Body: {resp.text()}"
            )
