import allure
import pytest

from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.content_library.edit_content_page import EditContentPage
from src.page_objects.entity.content_library_entity import (
    ContentLibraryEntity,
    ContentLibraryEntityFactory,
)


@pytest.mark.parametrize(
    'user,education_content',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ContentLibraryEntityFactory.get_edited_quiz_content(),
            marks=allure.testcase('31635'),
        )
    ],
)
@pytest.mark.smoke
@pytest.mark.web
def test_edit_quiz_content(
    quiz_edit_content_page: EditContentPage, education_content: ContentLibraryEntity
):
    quiz_edit_content_page.edit_content(education_content)


@pytest.mark.parametrize(
    'user,education_content',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ContentLibraryEntityFactory.get_edited_quiz_content(),
            marks=allure.testcase('31635'),
        )
    ],
)
@pytest.mark.smoke
@pytest.mark.web
def test_edit_quiz_video_content(
    quiz_video_edit_content_page: EditContentPage,
    education_content: ContentLibraryEntity,
):
    quiz_video_edit_content_page.edit_content(education_content)


@pytest.mark.parametrize(
    'user,education_content',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ContentLibraryEntityFactory.get_edited_survey_content(),
            marks=allure.testcase('31764'),
        )
    ],
)
@pytest.mark.smoke
@pytest.mark.web
def test_edit_survey_content(
    survey_edit_content_page: EditContentPage, education_content: ContentLibraryEntity
):
    survey_edit_content_page.edit_content(education_content)
