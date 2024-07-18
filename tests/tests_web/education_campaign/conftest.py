import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.models.education.education_content_model import EducationContentModel
from src.models.factories.education_campaign.education_campaign_model_factory import EducationCampaignModelFactory


@pytest.fixture(scope="function")
def education_campaign(api_request_context_customer_admin, api_request_context_aw_admin,
                       user: UserModel, employee_ids: list[int] = None) -> EducationCampaignDetailsModel:
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
    education_service = api.education(api_request_context_aw_admin)
    education_service.aw_admin_education_assignments(campaign_id=result.json()["id"])

    api_request_context = api_request_context_aw_admin if user.is_admin else api_request_context_customer_admin
    result = api.education(api_request_context).get_campaign_details(campaign_id=result.json()["id"])
    education_campaign = EducationCampaignDetailsModel.from_dict(result.json())
    return education_campaign


@pytest.fixture(scope="function")
def remove_education_campaign(request, education_campaign,
                              api_request_context_aw_admin) -> EducationCampaignDetailsModel:
    def finalizer():
        expect(education_service.delete_education_campaign(education_campaign.id)).to_be_ok()

    request.addfinalizer(finalizer)
    education_service = api.education(api_request_context_aw_admin)
    return education_campaign
