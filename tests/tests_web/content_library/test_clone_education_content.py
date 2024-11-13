import allure
import pytest

from src.apis.api_factory import api
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.content_library.const import ContentType
from src.page_objects.content_library.content_library_page import ContentLibraryPage


class TestCloneEducationContent:
    @pytest.mark.smoke
    @pytest.mark.web
    @pytest.mark.parametrize(
        'user,content_type',
        [
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentType.VIDEO,
                marks=allure.testcase('31788'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentType.VIDEO,
                marks=allure.testcase('31789'),
            ),
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentType.QUIZ,
                marks=allure.testcase('31790'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentType.QUIZ,
                marks=allure.testcase('31791'),
            ),
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentType.SLIDES,
                marks=allure.testcase('31792'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentType.SLIDES,
                marks=allure.testcase('31793'),
            ),
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentType.SURVEY,
                marks=allure.testcase('31796'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentType.SURVEY,
                marks=allure.testcase('31797'),
            ),
            pytest.param(
                UserModelFactory.aw_admin(),
                ContentType.PDF,
                marks=allure.testcase('31794'),
            ),
            pytest.param(
                UserModelFactory.customer_admin(),
                ContentType.PDF,
                marks=allure.testcase('31795'),
            ),
        ],
    )
    def test_clone_education_content(
        self,
        content_library_page: ContentLibraryPage,
        user: UserModel,
        content_type: ContentType,
        api_request_context_aw_admin,
        api_request_context_customer_admin,
    ):
        content_library_page.set_content_type_filter(content_type)
        content_library_details_page = (
            content_library_page.open_second_education_content()
        )
        content_library_entity = (
            content_library_details_page.get_content_library_entity(content_type)
        )

        content_library_details_page.clone_content()

        cloned_content_library_entity = (
            content_library_details_page.get_content_library_entity(content_type)
        )
        content_library_entity.title = 'Clone - ' + content_library_entity.title
        assert (
            content_library_entity == cloned_content_library_entity
        ), f'{content_library_entity=}\n\n{cloned_content_library_entity=}'
        if user.is_admin:
            assert eval(
                content_library_details_page.content_visibility.hidden_button.get_attribute(
                    'aria-pressed'
                ).title()
            ), 'hidden button is not selected by default after cloning scenario'
        request_context = (
            api_request_context_aw_admin
            if user.is_admin
            else api_request_context_customer_admin
        )
        education_content_service = api.education(request_context)
        education_content_service.delete_education_content(
            content_id=content_library_details_page.get_content_id()
        )
