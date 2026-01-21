"""Authentication fixtures - single source of truth."""
import json
import pytest
from typing import Generator
from filelock import FileLock
from playwright.sync_api import Playwright, APIRequestContext

from v2.src.core.config import Config


@pytest.fixture(scope="session")
def auth_state(playwright: Playwright, tmp_path_factory) -> str:
    """Login once with master token, save cookies for all."""
    root_tmp = tmp_path_factory.getbasetemp().parent
    auth_file = root_tmp / "auth_state.json"
    lock_file = root_tmp / "auth.lock"

    with FileLock(lock_file):
        if not auth_file.exists():
            request_context = playwright.request.new_context(
                base_url=Config.BASE_URL,
                extra_http_headers={"Authorization": f"Bearer {Config.MASTER_TOKEN}"}
            )
            resp = request_context.post("/api/auth/service-login")
            assert resp.ok, f"Service login failed: {resp.status}"
            request_context.storage_state(path=str(auth_file))
            request_context.dispose()

    return str(auth_file)


@pytest.fixture(scope="session")
def session_cookies(auth_state) -> dict:
    """Extract cookies for requests library."""
    with open(auth_state) as f:
        state = json.load(f)
    return {c["name"]: c["value"] for c in state.get("cookies", [])}