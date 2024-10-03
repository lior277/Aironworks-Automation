import allure
import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.education.education_content_model import EducationContentModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.content_library.add_content_page import AddContentPage
from src.page_objects.entity.content_library_entity import (
    ContentLibraryEntity,
    ContentLibraryEntityFactory,
)


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


class TestCreateEducationContent:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,education_content',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentLibraryEntityFactory.get_video_content(),
                marks=allure.testcase('31638'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentLibraryEntityFactory.get_video_content(),
                marks=allure.testcase('31647'),
            ),
        ],
    )
    def test_create_video_education_content(
        self,
        add_content_page: AddContentPage,
        user: UserModel,
        education_content: ContentLibraryEntity,
        remove_education_content,
    ):
        add_content_page.create_content(education_content, user)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,education_content',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentLibraryEntityFactory.get_pdf_content(),
                marks=allure.testcase('31642'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentLibraryEntityFactory.get_pdf_content(),
                marks=allure.testcase('31649'),
            ),
        ],
    )
    def test_create_pdf_education_content(
        self,
        add_content_page: AddContentPage,
        user: UserModel,
        education_content: ContentLibraryEntity,
        remove_education_content,
    ):
        add_content_page.create_content(education_content, user)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,education_content',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentLibraryEntityFactory.get_slides_content(),
                marks=allure.testcase('31640'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentLibraryEntityFactory.get_slides_content(),
                marks=allure.testcase('31648'),
            ),
        ],
    )
    def test_create_slides_education_content(
        self,
        add_content_page: AddContentPage,
        user: UserModel,
        education_content: ContentLibraryEntity,
        remove_education_content,
    ):
        add_content_page.create_content(education_content, user)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,education_content',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentLibraryEntityFactory.get_quiz_content(),
                marks=allure.testcase('31635'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentLibraryEntityFactory.get_quiz_content(),
                marks=allure.testcase('31650'),
            ),
        ],
    )
    def test_create_quiz_education_content(
        self,
        add_content_page: AddContentPage,
        user: UserModel,
        education_content: ContentLibraryEntity,
        remove_education_content,
    ):
        add_content_page.create_content(education_content, user)

    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,education_content',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentLibraryEntityFactory.get_survey_content(),
                marks=allure.testcase('31764'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentLibraryEntityFactory.get_survey_content(),
                marks=allure.testcase('31765'),
            ),
        ],
    )
    def test_create_survey_education_content(
        self,
        add_content_page: AddContentPage,
        user: UserModel,
        education_content: ContentLibraryEntity,
        remove_education_content,
    ):
        add_content_page.create_content(education_content, user)
