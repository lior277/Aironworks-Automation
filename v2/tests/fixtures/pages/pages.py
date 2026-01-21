"""UI Page Object fixtures."""

import pytest

from v2.src.core.config import Config
from v2.src.ui.pages.campaign_details_page import CampaignDetailsPage
from v2.src.ui.pages.campaigns_page import CampaignsPage
from v2.src.ui.pages.content_library_page import ContentLibraryPage
from v2.src.ui.pages.dashboard_page import DashboardPage
from v2.src.ui.pages.education_campaign_page import EducationCampaignPage
from v2.src.ui.pages.email_filter_page import EmailFilterPage
from v2.src.ui.pages.employees_page import EmployeesPage
from v2.src.ui.pages.groups_page import GroupsPage

# Import all page classes
from v2.src.ui.pages.login_page import LoginPage
from v2.src.ui.pages.operations_page import OperationsPage
from v2.src.ui.pages.scenarios_page import ScenariosPage
from v2.src.ui.pages.training_settings_page import TrainingSettingsPage

# =========================
# Core Pages
# =========================


@pytest.fixture
def login_page(page) -> LoginPage:
    """Login page - use for login tests only."""
    page.goto(f'{Config.BASE_URL}/login')
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page) -> DashboardPage:
    """Dashboard page - main entry point."""
    page.goto(f'{Config.BASE_URL}/dashboard')
    return DashboardPage(page)


# =========================
# Campaign Pages
# =========================


@pytest.fixture
def campaigns_page(page) -> CampaignsPage:
    """Campaigns list page."""
    page.goto(f'{Config.BASE_URL}/campaigns')
    return CampaignsPage(page)


@pytest.fixture
def campaign_details_page(page, test_campaign) -> CampaignDetailsPage:
    """Campaign details page with test data."""
    page.goto(f'{Config.BASE_URL}/campaigns/{test_campaign["id"]}')
    return CampaignDetailsPage(page)


@pytest.fixture
def scenarios_page(page) -> ScenariosPage:
    """Scenarios page."""
    page.goto(f'{Config.BASE_URL}/scenarios')
    return ScenariosPage(page)


# =========================
# Employee Pages
# =========================


@pytest.fixture
def employees_page(page) -> EmployeesPage:
    """Employee directory page."""
    page.goto(f'{Config.BASE_URL}/employees')
    return EmployeesPage(page)


@pytest.fixture
def groups_page(page) -> GroupsPage:
    """Groups page."""
    page.goto(f'{Config.BASE_URL}/groups')
    return GroupsPage(page)


# =========================
# Education Pages
# =========================


@pytest.fixture
def education_campaign_page(page) -> EducationCampaignPage:
    """Education campaign page."""
    page.goto(f'{Config.BASE_URL}/education/campaigns')
    return EducationCampaignPage(page)


@pytest.fixture
def content_library_page(page) -> ContentLibraryPage:
    """Content library page."""
    page.goto(f'{Config.BASE_URL}/education/content')
    return ContentLibraryPage(page)


# =========================
# Operations Pages
# =========================


@pytest.fixture
def operations_page(page) -> OperationsPage:
    """Operations page."""
    page.goto(f'{Config.BASE_URL}/operations')
    return OperationsPage(page)


# =========================
# Settings Pages
# =========================


@pytest.fixture
def training_settings_page(page) -> TrainingSettingsPage:
    """Training settings page."""
    page.goto(f'{Config.BASE_URL}/settings/training')
    return TrainingSettingsPage(page)


@pytest.fixture
def email_filter_page(page) -> EmailFilterPage:
    """Email filter settings page."""
    page.goto(f'{Config.BASE_URL}/settings/email-filter')
    return EmailFilterPage(page)
