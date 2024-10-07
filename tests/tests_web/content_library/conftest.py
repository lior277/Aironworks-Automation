import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.education.education_content_model import EducationContentModel
from src.page_objects.entity.content_library_entity import ContentLibraryEntity


@pytest.fixture(scope='function')
def remove_education_content(
    request,
    api_request_context_aw_admin,
    user: UserModel,
    api_request_context_customer_admin,
    education_content: ContentLibraryEntity,
):
    def finalizer():
        request_context = (
            api_request_context_aw_admin
            if user.is_admin
            else api_request_context_customer_admin
        )
        education_content_service = api.education(request_context)
        response = education_content_service.get_content_pagination()
        expect(response).to_be_ok()
        content = EducationContentModel.from_dict(response.json())
        response = education_content_service.get_content_pagination(limit=content.total)
        expect(response).to_be_ok()
        content = EducationContentModel.from_dict(response.json())
        out = [item for item in content.items if item.title == education_content.title]
        assert len(out) > 0
        expect(education_content_service.delete_education_content(out[0].id)).to_be_ok()

    request.addfinalizer(finalizer)
