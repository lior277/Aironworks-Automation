import allure
import pytest

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.education_campaign.education_campaign_page import (
    EducationCampaignPage,
)
from src.page_objects.entity.education_campaign_entity import EducationCampaignFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(UserModelFactory.aw_admin(), marks=allure.testcase('31525')),
        pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('31526')),
        pytest.param(UserModelFactory.aw_admin(), marks=allure.testcase('31525')),
        pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('31526')),
    ],
)
def test_view_education_campaign(
    remove_education_campaign,
    education_campaign_page: EducationCampaignPage,
    user: UserModel,
):
    actual_education_campaign = education_campaign_page.get_education_campaign(
        remove_education_campaign.title
    )
    expected_education_campaign = EducationCampaignFactory.get_education_campaign(
        remove_education_campaign
    )
    assert actual_education_campaign == expected_education_campaign, (
        f'{actual_education_campaign=}\n{expected_education_campaign=}'
    )


@pytest.mark.parametrize(
    'user, total, field, value, record',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            6,
            'Email',
            'pham.duc',
            1,
            id='AW Admin',
            marks=allure.testcase('31549'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            6,
            'Email',
            'pham.duc',
            1,
            id='Customer Admin',
            marks=allure.testcase('31552'),
        ),
    ],
)
@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.smoke
def test_education_campaign_detail(
    view_education_campaign_details_page: EducationCampaignPage,
    user,
    total,
    field,
    value,
    record,
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    view_education_campaign_details_page.filter_assignments(field, value, record)
