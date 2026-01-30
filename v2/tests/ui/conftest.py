"""UI-specific fixtures."""

import pytest

from v2.src.pages.ui_pages.campaigns_page import CampaignsPage


@pytest.fixture
def campaigns_page(page) -> CampaignsPage:
    """Campaigns page object."""
    return CampaignsPage(page)
