"""Main conftest - imports all fixtures."""
import sys
import pytest

pytest_plugins = [
    "v2.tests.fixtures.auth",
    "v2.tests.fixtures.browser",
    "v2.tests.fixtures.data",
    "v2.tests.fixtures.email",
    "v2.tests.fixtures.allure",
    "v2.tests.fixtures.pages.dashboard",
    "v2.tests.fixtures.pages.campaigns",
    "v2.tests.fixtures.pages.employees",
    "v2.tests.fixtures.pages.education",
    "v2.tests.fixtures.pages.settings",
]


def is_debug():
    return sys.monitoring.get_tool(sys.monitoring.DEBUGGER_ID) is not None


def pytest_collection_modifyitems(session, config, items):
    if not is_debug():
        for item in items:
            if item.get_closest_marker('timeout') is None:
                item.add_marker(pytest.mark.timeout(3 * 60))

    for item in items:
        for marker in item.iter_markers(name='allure_link'):
            test_id = 'C' + marker.args[0].split('/')[-1]
            item.user_properties.append(('test_id', test_id))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)