import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.content_library.create_campaign_page import CreateCampaignPage
from src.page_objects.dashboard_page import DashboardPage


class TestCreateVideoEducationCampaign:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), marks=pytest.mark.test_id("C931525")),
                                      pytest.param(UserModelFactory.customer_admin(),
                                                   marks=pytest.mark.test_id("C931526"))])
    def test_create_education_campaign(self, get_education_content, dashboard_page: DashboardPage,
                                       user: UserModel):
        create_campaign_page = CreateCampaignPage(dashboard_page.page).open(get_education_content.id)
        create_campaign_page.create_campaign()
