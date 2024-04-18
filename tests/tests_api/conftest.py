import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext, expect
from src.configs.config_loader import AppConfigs
from src.models.factories.user_model_factory import UserModelFactory
from src.apis.login import LoginService


@pytest.fixture(scope="session")
def api_request_context_customer_admin(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    base_url = AppConfigs.BASE_URL
    # Get service account email and load the json data from the service account key file.

    request_context = playwright.request.new_context(base_url=base_url)
    expect(LoginService.login(request_context, UserModelFactory.my_user())).to_be_ok()
    yield request_context
    request_context.dispose()
