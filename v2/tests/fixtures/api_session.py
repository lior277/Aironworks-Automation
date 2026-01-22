"""ApiSession fixture (Playwright request context wrapper)."""

import pytest
from playwright.sync_api import APIRequestContext

from v2.src.core.http.api_session import ApiSession


@pytest.fixture(scope='session')
def api_session(api_context: APIRequestContext) -> ApiSession:
    """Reusable API session (per worker)."""
    return ApiSession(api_context)
