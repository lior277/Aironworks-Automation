"""Main conftest - shared fixtures for all tests."""

import tempfile
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    expect,
    sync_playwright,
)

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config

# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line('markers', 'smoke: Quick smoke tests')
    config.addinivalue_line('markers', 'regression: Full regression suite')
    config.addinivalue_line('markers', 'api: API tests')
    config.addinivalue_line('markers', 'ui: UI tests')


def pytest_runtest_makereport(item, call):
    """Hook to capture test result for fixtures."""
    if call.when == 'call':
        item.rep_call = call


# ============================================================================
# SESSION FIXTURES - Playwright & Browser
# ============================================================================


@pytest.fixture(scope='session')
def playwright() -> Generator[Playwright, None, None]:
    """Playwright instance for entire test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope='session')
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """Browser instance (session-scoped for performance)."""
    browser = playwright.chromium.launch(
        headless=Config.HEADLESS, args=['--disable-blink-features=AutomationControlled']
    )
    yield browser
    browser.close()


# ============================================================================
# AUTHENTICATION FIXTURES
# ============================================================================


def _get_worker_id(request) -> str:
    """Get pytest-xdist worker ID."""
    if hasattr(request.config, 'workerinput'):
        return request.config.workerinput['workerid']
    return 'master'


@pytest.fixture(scope='session')
def auth_dir(tmp_path_factory) -> Path:
    """Directory for auth storage states."""
    return tmp_path_factory.mktemp('auth')


@pytest.fixture(scope='session')
def auth_state_file(request, playwright: Playwright, auth_dir: Path) -> str:
    """
    Authenticate once per worker and save storage state.

    Returns path to storage_state.json with cookies.
    """
    worker_id = _get_worker_id(request)
    auth_file = auth_dir / f'storage_state_{worker_id}.json'

    # Return cached auth if exists
    if auth_file.exists():
        return str(auth_file)

    # Perform authentication
    api_context = playwright.request.new_context(base_url=Config.BASE_URL)

    try:
        with allure.step(f'[Worker: {worker_id}] Authentication Flow'):
            # Step 1: Login
            with allure.step('POST /api/auth/login'):
                login_resp = api_context.post(
                    AuthRoutes.LOGIN,
                    data={
                        'email': Config.USER_EMAIL,
                        'password': Config.USER_PASSWORD,
                        'remember': True,
                        'otp': '',
                        'admin': False,
                    },
                )
                assert login_resp.ok, f'Login failed: {login_resp.status}'

            # Step 2: Get user info
            with allure.step('GET /api/auth/info'):
                info_resp = api_context.get(AuthRoutes.INFO)
                assert info_resp.ok, f'Get info failed: {info_resp.status}'

                roles = info_resp.json().get('user', {}).get('roles', [])
                assert roles, 'No roles available'

            # Step 3: Pick role
            with allure.step('POST /api/auth/pick_role'):
                role_id = Config.USER_ROLE_ID or roles[0]['id']
                pick_resp = api_context.post(
                    AuthRoutes.PICK_ROLE, data={'role_id': role_id}
                )
                assert pick_resp.ok, f'Pick role failed: {pick_resp.status}'

            # Save storage state
            api_context.storage_state(path=str(auth_file))

    finally:
        api_context.dispose()

    return str(auth_file)


# ============================================================================
# BROWSER CONTEXT & PAGE FIXTURES
# ============================================================================


def _safe_title(page: Page) -> str:
    """Safely get page title."""
    try:
        return page.title()
    except Exception:
        return 'unknown'


@pytest.fixture
def context(
    request, browser: Browser, auth_state_file: str
) -> Generator[BrowserContext, None, None]:
    """
    Browser context with authentication.
    Fresh context per test with tracing.
    """
    # Create context with auth
    ctx = browser.new_context(
        storage_state=auth_state_file, viewport={'width': 1440, 'height': 900}
    )

    # Configure timeouts
    ctx.set_default_timeout(Config.DEFAULT_TIMEOUT * 1000)
    expect.set_options(timeout=20_000)

    # Start tracing
    ctx.tracing.start(name=request.node.name, screenshots=True, snapshots=True)

    yield ctx

    # On test failure: save trace and screenshots
    test_failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed

    if test_failed:
        # Save trace
        trace_path = tempfile.mktemp(prefix='trace_', suffix='.zip')
        ctx.tracing.stop(path=trace_path)
        allure.attach.file(
            trace_path, name='trace.zip', attachment_type=allure.attachment_type.ZIP
        )

        # Screenshot all pages
        for pg in ctx.pages:
            try:
                allure.attach(
                    pg.screenshot(full_page=True),
                    name=f'{_safe_title(pg)}.png',
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
    else:
        ctx.tracing.stop()

    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """Fresh page per test."""
    return context.new_page()
