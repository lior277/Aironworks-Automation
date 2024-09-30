import pytest

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.scenario_model_factory import ScenarioModelFactory
from src.models.scenario import CampaignType, TargetDetails, TargetType
from src.models.scenario_model import ScenarioModel
from src.page_objects.scenarios_page import ScenariosPage


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(),
            id='test create scenario customer admin',
            marks=pytest.mark.test_id('C31490'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(target_type=TargetType.EMPLOYEE)
            ),
            id='test create scenario aw admin attack employee general',
            marks=pytest.mark.test_id('C31780'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(target_type=TargetType.COMPANY)
            ),
            id='test create scenario aw admin attack company general',
            marks=pytest.mark.test_id('C31779'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(
                    target_type=TargetType.EMPLOYEE,
                    target_company=AppConfigs.QA_COMPANY_NAME,
                )
            ),
            id='test create scenario aw admin attack company targeted',
            marks=pytest.mark.test_id('C31781'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(
                    target_type=TargetType.COMPANY,
                    target_company=AppConfigs.QA_COMPANY_NAME,
                )
            ),
            id='test create scenario aw admin attack employee targeted',
            marks=pytest.mark.test_id('C5991'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_APPLE),
            id='test create Apple data entry scenario customer admin',
            marks=pytest.mark.test_id('C31772'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_APPLE),
            id='test create Apple data entry scenario aw admin',
            marks=pytest.mark.test_id('C31775'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_GOOGLE),
            id='test create Google data entry scenario customer admin',
            marks=pytest.mark.test_id('C31771'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_GOOGLE),
            id='test create Google data entry scenario aw admin',
            marks=pytest.mark.test_id('C31774'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.DATA_ENTRY_MICROSOFT
            ),
            id='test create Microsoft data entry scenario customer admin',
            marks=pytest.mark.test_id('C31773'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.DATA_ENTRY_MICROSOFT
            ),
            id='test create Microsoft data entry scenario aw admin',
            marks=pytest.mark.test_id('C31776'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_data_entry_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.create_scenario(scenario)
