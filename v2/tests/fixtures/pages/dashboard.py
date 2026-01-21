"""Dashboard page fixtures."""
import pytest
from v2.src.ui.pages.dashboard_page import DashboardPage
from v2.src.core.config import Config


@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    """Navigate to dashboard."""
    page.goto(f"{Config.BASE_URL}/dashboard")
    return DashboardPage(page)