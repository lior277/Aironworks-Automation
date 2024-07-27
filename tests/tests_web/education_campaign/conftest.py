import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppConfigs
from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.company.employee_list_ids_model import EmployeeListIdsModel
from src.models.education.education_campaign_model import EducationCampaignDetailsModel
from src.models.education.education_content_model import EducationContentModel, Item
from src.models.factories.education_campaign.education_campaign_model_factory import (
    EducationCampaignModelFactory,
)


@pytest.fixture(scope="function")
def get_education_content(
    api_request_context_customer_admin, api_request_context_aw_admin, user: UserModel
) -> Item:
    api_request_context = (
        api_request_context_aw_admin
        if user.is_admin
        else api_request_context_customer_admin
    )
    education = api.education(api_request_context)
    response = education.get_content_pagination()
    expect(response).to_be_ok()
    content = EducationContentModel.from_dict(response.json())
    response = education.get_content_pagination(limit=content.total)
    expect(response).to_be_ok()
    content = EducationContentModel.from_dict(response.json())
    if user.is_admin:
        out = [item for item in content.items if item.any_company]
    else:
        out = [item for item in content.items]
    assert len(out) > 0
    return out[0]


@pytest.fixture(scope="function")
def education_campaign(
    api_request_context_customer_admin,
    api_request_context_aw_admin,
    user: UserModel,
    employee_ids: list[int] = None,
) -> EducationCampaignDetailsModel:
    company = api.company(api_request_context_customer_admin)
    education = api.education(api_request_context_customer_admin)
    if not employee_ids:
        response = company.get_employee_ids(
            EmployeeListIdsModel(employee_role=True, filters=None)
        )
        employee_ids = response.json()["items"][:1]
    education_campaign = (
        EducationCampaignModelFactory.get_education_campaign_from_education_content(
            AppConfigs.EXAMPLE_EDUCATION_CONTENT, employee_ids
        )
    )
    result = education.start_campaign(education_campaign)
    expect(result).to_be_ok()
    assert "id" in result.json()
    education_service = api.education(api_request_context_aw_admin)
    education_service.aw_admin_education_assignments(campaign_id=result.json()["id"])

    api_request_context = (
        api_request_context_aw_admin
        if user.is_admin
        else api_request_context_customer_admin
    )
    result = api.education(api_request_context).get_campaign_details(
        campaign_id=result.json()["id"]
    )
    education_campaign = EducationCampaignDetailsModel.from_dict(result.json())
    return education_campaign


@pytest.fixture(scope="function")
def remove_education_campaign(
    request, education_campaign, api_request_context_aw_admin
) -> EducationCampaignDetailsModel:
    def finalizer():
        expect(
            education_service.delete_education_campaign(education_campaign.id)
        ).to_be_ok()

    request.addfinalizer(finalizer)
    education_service = api.education(api_request_context_aw_admin)
    return education_campaign
