import os

import allure
import pytest

from src.configs.config_loader import AppConfigs, AppFolders
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
            marks=allure.testcase('31490'),
        ),
        pytest.param(
            UserModelFactory.encrypted_customer_admin(),
            ScenarioModelFactory.scenario(),
            id='test create scenario customer admin',
            marks=[
                allure.testcase('31490'),
                pytest.mark.skipif(
                    os.getenv('ENV') != 'staging', reason='Staging only'
                ),
            ],
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(target_type=TargetType.EMPLOYEE)
            ),
            id='test create scenario aw admin attack employee general',
            marks=allure.testcase('31780'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                target_details=TargetDetails(target_type=TargetType.COMPANY)
            ),
            id='test create scenario aw admin attack company general',
            marks=allure.testcase('31779'),
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
            marks=allure.testcase('31781'),
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
            marks=allure.testcase('5991'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_APPLE),
            id='test create Apple data entry scenario customer admin',
            marks=allure.testcase('31772'),
        ),
        pytest.param(
            UserModelFactory.encrypted_customer_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_APPLE),
            id='test create Apple data entry scenario customer admin',
            marks=[
                allure.testcase('31772'),
                pytest.mark.skipif(
                    os.getenv('ENV') != 'staging', reason='Staging only'
                ),
            ],
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_APPLE),
            id='test create Apple data entry scenario aw admin',
            marks=allure.testcase('31775'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_GOOGLE),
            id='test create Google data entry scenario customer admin',
            marks=allure.testcase('31771'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(campaign_type=CampaignType.DATA_ENTRY_GOOGLE),
            id='test create Google data entry scenario aw admin',
            marks=allure.testcase('31774'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.DATA_ENTRY_MICROSOFT
            ),
            id='test create Microsoft data entry scenario customer admin',
            marks=allure.testcase('31773'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.DATA_ENTRY_MICROSOFT
            ),
            id='test create Microsoft data entry scenario aw admin',
            marks=allure.testcase('31776'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_data_entry_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(
                html_content=None,
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.pdf'),
            ),
            id='test create attachment scenario customer admin',
            marks=allure.testcase('31783'),
        ),
        pytest.param(
            UserModelFactory.encrypted_customer_admin(),
            ScenarioModelFactory.scenario(
                html_content=None,
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.pdf'),
            ),
            id='test create attachment scenario customer admin',
            marks=[
                allure.testcase('31783'),
                pytest.mark.skipif(
                    os.getenv('ENV') != 'staging', reason='Staging only'
                ),
            ],
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                html_content=None,
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.pdf'),
            ),
            id='test create attachment scenario aw admin',
            marks=allure.testcase('31782'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_attachment_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    'user,scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.txt'),
            ),
            id='test create attachment scenario customer admin',
            marks=allure.testcase('31784'),
        ),
        pytest.param(
            UserModelFactory.encrypted_customer_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.txt'),
            ),
            id='test create attachment scenario customer admin',
            marks=[
                allure.testcase('31784'),
                pytest.mark.skipif(
                    os.getenv('ENV') != 'staging', reason='Staging only'
                ),
            ],
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            ScenarioModelFactory.scenario(
                campaign_type=CampaignType.ATTACHMENT,
                file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.txt'),
            ),
            id='test create attachment scenario aw admin',
            marks=allure.testcase('31785'),
        ),
    ],
)
@pytest.mark.smoke
def test_create_attachment_scenario_with_unsupported_file_extension(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.navigate_create_scenario()
    scenarios_page.select_content_type(scenario)


@pytest.mark.parametrize(
    'user, scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(vector='SMS'),
        )
    ],
)
@pytest.mark.smoke
def test_create_sms_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.create_scenario(scenario)


@pytest.mark.parametrize(
    'user, scenario',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            ScenarioModelFactory.scenario(vector='Web'),
        )
    ],
)
@pytest.mark.smoke
def test_create_web_scenario(
    user: UserModel, scenario: ScenarioModel, scenarios_page: ScenariosPage
):
    scenarios_page.create_scenario(scenario)


@pytest.mark.smoke
@pytest.mark.parametrize(
    'user, number_of_scenarios, level, language, sender, real_name, additional_info',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            '1',
            '4 Advanced',
            'English',
            'Internal',
            'Department',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            '2',
            '3 Intermediate',
            'English',
            'External',
            'Company',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            '3',
            '2 Basic',
            'English',
            'Internal',
            'Impersonal',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            '1',
            '1 Easy',
            'Japanese',
            'Internal',
            'Department',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            '2',
            '3 Intermediate',
            'Japanese',
            'External',
            'Impersonal',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            '3',
            '5 Sophisticated',
            'English',
            'Internal',
            'Person',
            None,
            id='test create AI generated scenario customer admin',
            marks=[allure.testcase('31786'), pytest.mark.xdist_group(name='agent1')],
        ),
    ],
)
def test_request_ai_generated_scenario(
    user: UserModel,
    scenarios_page: ScenariosPage,
    number_of_scenarios,
    level,
    language,
    sender,
    real_name,
    additional_info,
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    request_ai_scenario_page = scenarios_page.navigate_request_ai_generated_scenario()
    request_ai_scenario_page.generate_scenario(
        number_of_scenarios, level, language, sender, real_name
    )
    scenarios_page.save_button.click()
    scenarios_page.ensure_alert_message_is_visible('Created new scenario')
