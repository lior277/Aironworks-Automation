import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.education_campaign.education_campaign_page import EducationCampaignPage
from src.page_objects.entity.education_campaign_entity import EducationCampaignFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), marks=pytest.mark.test_id("C31525")),
                                  pytest.param(UserModelFactory.customer_admin(), marks=pytest.mark.test_id("C31526"))])
def test_view_education_campaign(remove_education_campaign, education_campaign_page: EducationCampaignPage,
                                 user: UserModel):
    actual_education_campaign = education_campaign_page.get_education_campaign(remove_education_campaign.title)
    expected_education_campaign = EducationCampaignFactory.get_education_campaign(remove_education_campaign)
    assert actual_education_campaign == expected_education_campaign, \
        f"{actual_education_campaign=}\n{expected_education_campaign=}"
