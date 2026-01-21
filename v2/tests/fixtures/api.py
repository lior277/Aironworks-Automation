"""API fixtures."""
import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext

from v2.src.core.config import Config
from v2.src.core.http.api_session import ApiSession


@pytest.fixture(scope="session")
def api_session(session_cookies) -> ApiSession:
    """Requests-based API client with shared auth."""
    session = ApiSession(base_url=Config.BASE_URL)
    session.set_cookies(session_cookies)
    return session


@pytest.fixture(scope="session")
def api_context(playwright: Playwright, auth_state) -> Generator[APIRequestContext, None, None]:
    """Playwright API with shared auth."""
    context = playwright.request.new_context(
        base_url=Config.BASE_URL,
        storage_state=auth_state
    )
    yield context
    context.dispose()