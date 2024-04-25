import pytest
from src.utils.mailtrap import MailTrap


@pytest.fixture(scope="session")
def mailtrap(playwright):
    mailtrap = MailTrap(playwright)
    yield mailtrap
    mailtrap.close()


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))
