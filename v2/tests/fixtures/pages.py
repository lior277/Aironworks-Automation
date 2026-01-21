"""UI Page Object fixtures - page objects receive page with auth."""
import pytest

from v2.src.core.config import Config
from v2.src.ui.pages.dashboard_page import DashboardPage
from v2.src.ui.pages.campaigns_page import CampaignsPage
from v2.src.ui.pages.login_page import LoginPage


@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    """Dashboard page - already authenticated via context."""
    page.goto(f"{Config.BASE_URL}/dashboard")
    return DashboardPage(page)


@pytest.fixture
def campaigns_page(page) -> CampaignsPage:
    """Campaigns page - already authenticated via context."""
    page.goto(f"{Config.BASE_URL}/campaigns")
    return CampaignsPage(page)