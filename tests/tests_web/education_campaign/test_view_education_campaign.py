import pytest

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.education_campaign.education_campaign_page import EducationCampaignPage
from src.page_objects.entity.education_campaign_entity import EducationCampaignFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), marks=pytest.mark.test_id("C31525")),
                                  pytest.param(UserModelFactory.customer_admin(), marks=pytest.mark.test_id("C31526"))])
def test_view_education_campaign(create_education_campaign, api_request_context_aw_admin,
                                 api_request_context_customer_admin, education_campaign_page: EducationCampaignPage,
                                 user: UserModel):
    api_request_context = api_request_context_aw_admin if user.is_admin else api_request_context_customer_admin

    result = api.education(api_request_context).get_campaign_details(campaign_id=create_education_campaign)
    education_campaign_model = EducationCampaignDetailsModel.from_dict(result.json())
    actual_education_campaign = education_campaign_page.get_education_campaign(education_campaign_model.title)
    expected_education_campaign = EducationCampaignFactory.get_education_campaign(education_campaign_model)
    assert actual_education_campaign == expected_education_campaign, \
        f"{actual_education_campaign=}\n{expected_education_campaign=}"
