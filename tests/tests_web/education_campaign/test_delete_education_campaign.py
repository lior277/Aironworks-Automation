import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.models.education.education_content_model import EducationContentModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.education_campaign.education_campaign_model_factory import EducationCampaignModelFactory
from src.page_objects.education_campaign.education_campaign_details_page import EducationCampaignDetailsPage


class TestDeleteEducationCampaign:

    @pytest.fixture(scope="function")
    def education_campaign(self, api_request_context_customer_admin,
                           employee_ids: list[int] = None) -> EducationCampaignDetailsModel:
        company = api.company(api_request_context_customer_admin)
        education = api.education(api_request_context_customer_admin)
        if not employee_ids:
            response = company.get_employee_ids(EmployeeListIdsModel(employee_role=True, filters=None))
            employee_ids = response.json()["items"][:1]
        response = education.get_content_pagination()
        assert response.ok, f"Failed to fetch education content => {response.json()}"
        education_content = EducationContentModel.from_dict(response.json())
        education_campaign = EducationCampaignModelFactory.get_education_campaign_from_education_content(
            education_content.items[0], employee_ids)
        result = education.start_campaign(education_campaign)
        expect(result).to_be_ok()
        assert "id" in result.json()
        return EducationCampaignDetailsModel.from_dict(result.json())

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), marks=pytest.mark.test_id("C31628")),
                                      pytest.param(UserModelFactory.customer_admin(),
                                                   marks=pytest.mark.test_id("C31625"))])
    def test_delete_education_campaign(self, education_campaign: EducationCampaignDetailsModel,
                                       education_campaign_detail_page: EducationCampaignDetailsPage, user: UserModel):
        education_campaign_detail_page.delete_campaign()
