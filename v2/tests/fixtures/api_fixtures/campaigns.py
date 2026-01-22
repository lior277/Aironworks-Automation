"""Campaign page fixtures."""

import pytest
from playwright.sync_api import APIRequestContext, Page

from v2.src.core.config import Config
from v2.src.pages import CampaignsPage, DashboardPage


@pytest.fixture
def dashboard_page(page: Page, api_context: APIRequestContext) -> DashboardPage:
    """Dashboard page with API context."""
    page.goto(f'{Config.BASE_URL}/dashboard')
    return DashboardPage(page, api_context)


@pytest.fixture
def campaigns_page(page: Page, api_context: APIRequestContext) -> CampaignsPage:
    """Campaigns page with API context."""
    page.goto(f'{Config.BASE_URL}/campaigns')
    return CampaignsPage(page, api_context)
