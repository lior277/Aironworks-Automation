"""Campaign page fixtures."""

import pytest

from v2.src.ui.pages.campaign_details_page import CampaignDetailsPage
from v2.src.ui.pages.campaigns_page import CampaignsPage


@pytest.fixture
def campaigns_page(dashboard_page) -> CampaignsPage:
    """Navigate to campaigns list."""
    return dashboard_page.navigation_bar.navigate_campaigns()


@pytest.fixture
def campaign_details_page(campaigns_page, test_campaign) -> CampaignDetailsPage:
    """Open campaign details."""
    return campaigns_page.open_campaign(test_campaign['id'])
