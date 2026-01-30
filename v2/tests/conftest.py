import os
import re
import tempfile
import time
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, expect

from v2.integrations.mailtrap.models import MailtrapConfig
from v2.integrations.mailtrap_client import MailtrapClient
from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.api.models.auth import LoginRequest
from v2.src.core.auth.api_auth import AuthService
from v2.src.core.config import Config
from v2.src.core.http.api_session import ApiSession
from v2.src.core.utils.allure_utils import AllureReporter

# =============================================================================
# Constants / Defaults
# =============================================================================

AUTH_CACHE_MAX_AGE_HOURS = 24.0

ALLURE_CATEGORIES = [
    {
        'name': 'Authentication Failures',
        'matchedStatuses': ['failed'],
        'messageRegex': '.*401.*|.*unauthorized.*|.*authentication.*',
    },
    {
        'name': 'Timeout Errors',
        'matchedStatuses': ['broken'],
        'messageRegex': '.*timeout.*|.*timed out.*',
    },
    {
        'name': 'Assertion Failures',
        'matchedStatuses': ['failed'],
        'messageRegex': '.*AssertionError.*',
    },
]

# =============================================================================
# CLI Options
# =============================================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        '--fresh-auth', action='store_true', help='Force fresh authentication'
    )
    parser.addoption(
        '--enable-tracing',
        action='store_true',
        help='Attach trace.zip on failed UI/hybrid tests',
    )


# =============================================================================
# Pytest Hooks
# =============================================================================


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f'rep_{report.when}', report)

    if report.when == 'call' and report.failed:
        allure.attach(str(report.longrepr), 'Stack Trace', allure.attachment_type.TEXT)


# =============================================================================
# Helpers
# =============================================================================


def _worker_id(request: pytest.FixtureRequest) -> str:
    worker_input = getattr(request.config, 'workerinput', None)
    if isinstance(worker_input, dict) and worker_input.get('workerid'):
        return str(worker_input['workerid'])
    return os.environ.get('PYTEST_XDIST_WORKER', 'master')


def _is_ui_test(request: pytest.FixtureRequest) -> bool:
    return (
        request.node.get_closest_marker('ui') is not None
        or request.node.get_closest_marker('web') is not None
    )


def _is_allure_writer(request: pytest.FixtureRequest) -> bool:
    # xdist: only gw0 writes one-time files; single worker: master writes
    return _worker_id(request) in {'master', 'gw0'}


def _allure_dir(request: pytest.FixtureRequest) -> Path:
    val = request.config.getoption('--alluredir', None)
    return Path(val) if val else Path('allure-results')


def _auth_cache_dir() -> Path:
    d = Path(tempfile.gettempdir()) / 'pytest-aironworks-auth'
    d.mkdir(parents=True, exist_ok=True)
    return d


def _is_fresh(path: Path, max_age_hours: float = AUTH_CACHE_MAX_AGE_HOURS) -> bool:
    if not path.exists():
        return False
    age_h = (time.time() - path.stat().st_mtime) / 3600
    return age_h < max_age_hours


def _verify_auth(playwright: Playwright, state_path: Path) -> bool:
    """Validate cached storage state by calling /api/auth/info."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=str(state_path)
    )
    try:
        ok = s.get(AuthRoutes.INFO).status == 200
        if ok:
            s.save_storage_state(state_path)  # persist rotated cookies
        return ok
    except Exception:
        return False
    finally:
        s.close()


def _configure_context(ctx: BrowserContext) -> None:
    ctx.set_default_timeout(Config.DEFAULT_TIMEOUT_SEC * 1000)
    expect.set_options(timeout=Config.EXPECT_TIMEOUT_MS)


def _did_test_fail(request: pytest.FixtureRequest) -> bool:
    # covers failures in setup (fixture errors) and in the test body (call)
    for phase in ('setup', 'call'):
        rep = getattr(request.node, f'rep_{phase}', None)
        if rep and rep.failed:
            return True
    return False


def _tracing_enabled_for_test(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption('--enable-tracing', False))


def _safe_filename(s: str) -> str:
    return re.sub(r'[^0-9A-Za-z._-]+', '_', s)


def _trace_output_path(request: pytest.FixtureRequest) -> Path:
    # Save traces OUTSIDE allure-results to avoid xdist collisions / file locks
    worker = _worker_id(request)
    node = _safe_filename(request.node.nodeid)
    base = Path(tempfile.gettempdir()) / 'pw-traces'
    base.mkdir(parents=True, exist_ok=True)
    return base / f'trace_{worker}_{node}_{time.time_ns()}.zip'


# =============================================================================
# One-time setup (session)
# =============================================================================


@pytest.fixture(scope='session', autouse=True)
def setup_allure_environment(request: pytest.FixtureRequest) -> None:
    allure_dir = _allure_dir(request)
    if not _is_allure_writer(request):
        return

    allure_dir.mkdir(parents=True, exist_ok=True)
    AllureReporter(str(allure_dir)).setup(
        env=Config.ENV, base_url=Config.APP_BASE_URL, categories=ALLURE_CATEGORIES
    )


# =============================================================================
# Auth / API (session)
# =============================================================================


@pytest.fixture(scope='session')
def login_request() -> LoginRequest:
    return LoginRequest(
        email=Config.CUSTOMER_EMAIL, password=Config.CUSTOMER_PASSWORD, admin=False
    )


@pytest.fixture(scope='session')
def auth_state_file(
    request: pytest.FixtureRequest, playwright: Playwright, login_request: LoginRequest
) -> str:
    worker = _worker_id(request)
    state_path = _auth_cache_dir() / f'storage_state_{Config.ENV}_{worker}.json'

    force_fresh = request.config.getoption('--fresh-auth', False)
    if force_fresh and state_path.exists():
        state_path.unlink()

    if (
        not force_fresh
        and _is_fresh(state_path)
        and _verify_auth(playwright, state_path)
    ):
        return str(state_path)

    s = ApiSession(playwright, base_url=Config.APP_BASE_URL)
    try:
        AuthService(
            s, login_request, role_id=Config.CUSTOMER_ROLE_ID or None
        ).login_and_save_state(state_path)
    finally:
        s.close()

    return str(state_path)


@pytest.fixture
def api_session(
    playwright: Playwright, auth_state_file: str
) -> Generator[ApiSession, None, None]:
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        yield s
    finally:
        try:
            s.save_storage_state(auth_state_file)
        except Exception:
            pass
        s.close()


# =============================================================================
# Browser contexts (session + function)
# =============================================================================


@pytest.fixture(scope='function')
def browser_context(
    browser: Browser, auth_state_file: str, request: pytest.FixtureRequest
) -> Generator[BrowserContext, None, None]:
    """Function context for UI tests (isolated). Trace is saved only on failure."""
    ctx = browser.new_context(
        storage_state=auth_state_file, viewport={'width': 1440, 'height': 900}
    )
    _configure_context(ctx)

    trace_this_test = _tracing_enabled_for_test(request)
    if trace_this_test:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=False)

    yield ctx

    if trace_this_test:
        try:
            if _did_test_fail(request):
                trace_path = _trace_output_path(request)
                ctx.tracing.stop(path=str(trace_path))

                #  robust attach (no allure.attachment_type.ZIP)
                allure.attach.file(str(trace_path), name='trace.zip', extension='zip')
            else:
                ctx.tracing.stop()
        except Exception as e:
            allure.attach(str(e), 'trace-capture-error', allure.attachment_type.TEXT)

    try:
        ctx.storage_state(path=auth_state_file)
    except Exception:
        pass
    ctx.close()


# =============================================================================
# Pages
# =============================================================================


@pytest.fixture
def page(browser_context: BrowserContext) -> Generator[Page, None, None]:
    p = browser_context.new_page()
    yield p
    p.close()


# =============================================================================
# Mailtrap (session)
# =============================================================================


@pytest.fixture(scope='session')
def mailtrap_api_session(playwright: Playwright) -> Generator[ApiSession, None, None]:
    if not Config.MAILTRAP_API_TOKEN or Config.MAILTRAP_ACCOUNT_ID <= 0:
        raise RuntimeError('MAILTRAP_API_TOKEN / MAILTRAP_ACCOUNT_ID are missing')

    s = ApiSession(
        playwright,
        base_url=Config.MAILTRAP_BASE_URL,
        enable_refresh=False,  # Mailtrap is not your app auth domain
        default_headers={'Api-Token': Config.MAILTRAP_API_TOKEN},  # <-- token used here
        retries=5,
        retry_on_status={429, 500, 502, 503, 504},
        retry_delay_sec=1.0,
    )
    try:
        yield s
    finally:
        s.close()


@pytest.fixture(scope='session')
def mailtrap_client(mailtrap_api_session: ApiSession) -> MailtrapClient:
    cfg = MailtrapConfig(
        account_id=Config.MAILTRAP_ACCOUNT_ID,
        api_prefix=Config.MAILTRAP_API_PREFIX,  # "/api" default; "/api_access" if 404
        timeout_s=Config.MAILTRAP_TIMEOUT_SEC,
        poll_interval_s=Config.MAILTRAP_POLL_INTERVAL_SEC,
        max_pages=Config.MAILTRAP_MAX_PAGES,
    )
    return MailtrapClient(api=mailtrap_api_session, cfg=cfg)
