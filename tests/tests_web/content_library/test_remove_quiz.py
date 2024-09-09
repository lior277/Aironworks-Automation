import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.education.education_content_model import EducationContentModel, Item
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario.clone_education_content_model_factory import (
    CloneEducationContentModelFactory,
)
from src.page_objects.content_library.content_library_details_page import (
    ContentLibraryDetailsPage,
)
from src.page_objects.dashboard_page import DashboardPage


@pytest.fixture(scope='function')
def cloned_education_content(
    request,
    api_request_context_aw_admin,
    user: UserModel,
    api_request_context_customer_admin,
) -> Item:
    def finalizer():
        expect(education.delete_education_content(cloned_content.id)).to_be_ok()

    request.addfinalizer(finalizer)
    request_context = (
        api_request_context_aw_admin
        if user.is_admin
        else api_request_context_customer_admin
    )
    education = api.education(request_context)
    response = education.get_content_pagination()
    expect(response).to_be_ok()
    content = EducationContentModel.from_dict(response.json())
    response = education.get_content_pagination(limit=content.total)
    expect(response).to_be_ok()
    content = EducationContentModel.from_dict(response.json())
    out = [
        item
        for item in content.items
        if item.title != 'Test Content for QA'
        for part in item.parts
        if 'QUESTION' in part.kind and 'SINGLE' in part.question_type
    ]

    response = education.get_education_content_details(out[0].id)
    expect(response).to_be_ok()
    education_content_details = Item.from_dict(response.json())
    education_content_to_clone = (
        CloneEducationContentModelFactory.get_education_content(
            education_content_details
        )
    )
    response = education.clone_education_content(education_content_to_clone)
    expect(response).to_be_ok()
    cloned_content = Item.from_dict(response.json())
    return cloned_content


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id='AW Admin',
            marks=pytest.mark.test_id('C31632'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=pytest.mark.test_id('C31633'),
        ),
    ],
)
@pytest.mark.smoke
def test_remove_quiz(
    user: UserModel, cloned_education_content: Item, dashboard_page: DashboardPage
):
    content_library_details_page = ContentLibraryDetailsPage(dashboard_page.page).open(
        cloned_education_content.id
    )
    content_library_details_page.remove_quiz()
