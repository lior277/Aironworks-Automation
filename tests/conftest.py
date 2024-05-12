import pytest
import random
from src.utils.mailtrap import MailTrap
from src.configs.config_loader import AppConfigs
from playwright.sync_api import Playwright, APIRequestContext, expect
from typing import Generator
from src.utils.service_account_utils import generate_jwt


@pytest.fixture(scope="session")
def mailtrap(playwright):
    mailtrap = MailTrap(playwright)
    yield mailtrap
    mailtrap.close()


@pytest.fixture(scope="session")
def example_mail():
    with open("tests/resources/example_mail.eml", "rb") as f:
        return f.read().replace(
            b"RANDOM_TEXT", str(random.randint(100000000, 999999999)).encode("utf-8")
        )


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))


@pytest.fixture(scope="session")
def api_request_context_addin(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.ADDIN_BASE_URL
    # Get service account email and load the json data from the service account key file.

    token = generate_jwt(
        AppConfigs.LOGIN_SA_ACCOUNT,
        audience=base_url,  # doesn't actually matter
    )
    headers = {"Authorization": "GG " + token}
    request_context = playwright.request.new_context(
        base_url=base_url, extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()
