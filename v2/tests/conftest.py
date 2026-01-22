"""Main conftest."""

import pytest

pytest_plugins = [
    'v2.tests.fixtures.auth',
    'v2.tests.fixtures.browser',
    'v2.tests.fixtures.pages',  # ← Single import for all pages
    'v2.tests.fixtures.allure',
]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)
