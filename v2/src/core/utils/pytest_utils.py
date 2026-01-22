"""Pytest helper utilities."""

import os
import sys

import pytest


def is_debug() -> bool:
    """Check if running in debugger."""
    return sys.monitoring.get_tool(sys.monitoring.DEBUGGER_ID) is not None


def should_skip_for_env(item) -> None:
    """
    Skip tests based on environment markers.

    Markers:
        - production_only: Skip if not on production
        - staging_only: Skip if not on staging
        - skip_ci: Skip if running in CI/CD
    """
    from v2.src.core.config import Config

    if item.get_closest_marker('production_only'):
        if not Config.ENV.startswith('production'):
            pytest.skip('Only runs on production')

    if item.get_closest_marker('staging_only'):
        if Config.ENV != 'staging':
            pytest.skip('Only runs on staging')

    if item.get_closest_marker('skip_ci'):
        if os.environ.get('CI'):
            pytest.skip('Skipped in CI')


def log_session_start() -> None:
    """Log test session start info."""
    from v2.src.core.config import Config

    print('\n' + '=' * 60)
    print('TEST SESSION STARTED')
    print(f'Environment: {Config.ENV}')
    print(f'Base URL: {Config.BASE_URL}')
    print('=' * 60 + '\n')


def log_session_end(exitstatus: int) -> None:
    """Log test session end."""
    print('\n' + '=' * 60)
    print(f'TEST SESSION FINISHED (exit: {exitstatus})')
    print('=' * 60 + '\n')


def log_summary(terminalreporter, config) -> None:
    """Print test summary."""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    errors = len(terminalreporter.stats.get('error', []))
    total = passed + failed + skipped + errors

    if total == 0:
        return

    pass_rate = (passed / total) * 100

    print('\n' + '=' * 60)
    print(f'SUMMARY: {passed}/{total} passed ({pass_rate:.1f}%)')
    print('=' * 60)

    allure_dir = config.getoption('--alluredir', None)
    if allure_dir:
        print(f'Allure: allure serve {allure_dir}\n')


def auto_add_markers(item) -> None:
    """Auto-add 'api' or 'ui' marker based on test path."""
    test_path = str(item.fspath)

    if '/api/' in test_path or '/tests_api/' in test_path:
        item.add_marker(pytest.mark.api)
    elif '/ui/' in test_path or '/tests_web/' in test_path:
        item.add_marker(pytest.mark.ui)
        item.add_marker(pytest.mark.web)


def extract_testrail_id(item) -> None:
    """Extract TestRail ID from @allure.link markers."""
    for marker in item.iter_markers(name='allure_link'):
        if marker.args:
            test_id = 'C' + str(marker.args[0]).split('/')[-1]
            item.user_properties.append(('test_id', test_id))
