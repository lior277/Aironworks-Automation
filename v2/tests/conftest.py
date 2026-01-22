import pytest
from playwright.sync_api import sync_playwright

from v2.src.core.config import Config
from v2.src.core.http.api_session import ApiSession

pytest_plugins = [
    'tests.fixtures.allure',
    'tests.fixtures.auth',
    'tests.fixtures.browser',
    'tests.fixtures.fixtures_ui',
    'tests.fixtures.fixtures_api',
]


@pytest.fixture(scope='session')
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='session')
def browser(playwright):
    browser = playwright.chromium.launch(headless=Config.HEADLESS)
    yield browser
    browser.close()


# -------- API SESSION (uses api_storage_state from auth.py) --------


@pytest.fixture
def api_session(playwright, api_storage_state):
    return ApiSession(playwright, api_storage_state)
