import pytest

from page_objects.campaigns_page import CampaignsPage


@pytest.fixture
def campaigns_page(page) -> CampaignsPage:
    return CampaignsPage(page)
