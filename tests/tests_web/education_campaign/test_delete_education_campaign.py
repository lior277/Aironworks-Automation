import pytest

from src.models.auth.user_model import UserModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.education_campaign.education_campaign_details_page import EducationCampaignDetailsPage


class TestDeleteEducationCampaign:

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), marks=pytest.mark.test_id("C31628")),
                                      pytest.param(UserModelFactory.customer_admin(),
                                                   marks=pytest.mark.test_id("C31625"))])
    def test_delete_education_campaign(self, education_campaign: EducationCampaignDetailsModel,
                                       education_campaign_detail_page: EducationCampaignDetailsPage, user: UserModel):
        education_campaign_detail_page.delete_campaign()
