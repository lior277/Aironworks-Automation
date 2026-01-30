"""API-specific fixtures."""

import pytest

from v2.src.core.http.api_session import ApiSession
from v2.src.pages.api_pages.campaign_service import CampaignService
from v2.src.pages.api_pages.scenario_service import ScenarioService


# conftest.py - Add campaign service fixture
@pytest.fixture
def campaign_service(api_session: ApiSession) -> CampaignService:
    """Campaign service with authenticated session"""
    return CampaignService(api_session)


# conftest.py - Add this fixture
@pytest.fixture
def scenario_service(api_session: ApiSession) -> ScenarioService:
    """Scenario service with authenticated session"""
    return ScenarioService(api_session)
