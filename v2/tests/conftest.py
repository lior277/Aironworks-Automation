"""Main conftest - imports all fixtures and defines hooks."""

import pytest

from v2.src.core.utils.pytest_helpers import (
    auto_add_markers,
    extract_testrail_id,
    is_debug,
    log_session_end,
    log_session_start,
    log_summary,
    should_skip_for_env,
)


def pytest_sessionstart(session):
    log_session_start()


def pytest_sessionfinish(session, exitstatus):
    log_session_end(exitstatus)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    log_summary(terminalreporter, config)


# =========================
# Import all fixtures
# =========================

pytest_plugins = [
    'v2.tests.fixtures.auth',
    'v2.tests.fixtures.api',
    'v2.tests.fixtures.api_clients',
    'v2.tests.fixtures.browser',
    'v2.tests.fixtures.data',
    'v2.tests.fixtures.pages',
    'v2.tests.fixtures.allure',
]


# =========================
# Hooks
# =========================


def pytest_runtest_setup(item):
    """Skip tests based on environment markers."""
    should_skip_for_env(item)


def pytest_collection_modifyitems(session, config, items):
    """Auto-add markers and extract test IDs."""
    for item in items:
        auto_add_markers(item)
        extract_testrail_id(item)

        # Remove timeout in debug mode
        if is_debug():
            item.own_markers = [m for m in item.own_markers if m.name != 'timeout']


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for fixtures (tracing on failure)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)
