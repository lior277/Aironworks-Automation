import pytest

from v2.src.pages.api_pages.campaigns_api import CampaignsApi


@pytest.fixture
def campaigns_api(api_session):
    return CampaignsApi(api_session)
