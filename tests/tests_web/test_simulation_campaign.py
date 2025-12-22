import csv
from datetime import datetime, timedelta

import allure
import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.campaign_details_page import CampaignDetailsPage
from src.page_objects.entity.campaign_attacks_summary_entity import (
    CampaignAttacksSummaryFactory,
)
from src.page_objects.scenarios_page import ScenariosPage
from src.utils.mailtrap import find_email


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id='AW Admin',
            marks=[allure.testcase('31544'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=[allure.testcase('31545'), pytest.mark.xdist_group(name='agent1')],
        ),
    ],
)
@pytest.mark.smoke
def test_create_simulation_campaign(
    user: UserModel, employee, scenarios_page: ScenariosPage, mailtrap
):
    scenario_name = AppConfigs.EXAMPLE_SCENARIO_NAME
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.filter.filter_by('Email', employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()
    execute_campaign_page.review_button.click()
    assert execute_campaign_page.number_of_employees.text_content() == '1'
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email), timeout=240
    )

    assert mail is not None, (
        f'Unable to find email {employee.email} please check the mailtrap inbox {AppConfigs.EMPLOYEE_INBOX_ID}'
    )


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=[allure.testcase('31545'), pytest.mark.xdist_group(name='agent1')],
        )
    ],
)
@pytest.mark.timeout(300)
@pytest.mark.smoke
def test_modify_simulation_campaign(
    user: UserModel,
    employee,
    mailtrap,
    first_campaign_details_page: CampaignDetailsPage,
):
    modify_campaign_page = (
        first_campaign_details_page.navigate_to_modify_campaign_page()
    )
    modify_campaign_page.edit_campaign(employee.email)
    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email), timeout=240
    )

    assert mail is not None, (
        f'Unable to find email {employee.email} please check the mailtrap inbox {AppConfigs.EMPLOYEE_INBOX_ID}'
    )


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id='AW Admin',
            marks=[allure.testcase('31547'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=[allure.testcase('31548'), pytest.mark.xdist_group(name='agent1')],
        ),
    ],
)
@pytest.mark.smoke
def test_create_simulation_campaign_scheduled(
    user: UserModel, employee, scenarios_page: ScenariosPage, mailtrap
):
    scenario_name = AppConfigs.EXAMPLE_SCENARIO_NAME
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    time_plus_one_day = datetime.now() + timedelta(days=1)
    formatted_time = time_plus_one_day.strftime('%m/%d/%Y %I:%M %p').lower()
    execute_campaign_page.select_time(formatted_time)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.filter.filter_by('Email', employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()
    execute_campaign_page.review_button.click()
    assert execute_campaign_page.number_of_employees.text_content() == '1'
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(), id='AW Admin', marks=allure.testcase('31547')
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=allure.testcase('31546'),
        ),
    ],
)
@pytest.mark.smoke
def test_campaigns_page_has_data(user, campaigns_page):
    tables = campaigns_page.page.get_by_test_id('table')
    expect(tables).to_have_count(2)
    campaigns_page.wait_for_tables_load()
    tables = tables.all()
    assert tables[0].get_by_role('row').count() >= 2
    assert tables[1].get_by_role('row').count() >= 2


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(), id='AW Admin', marks=allure.testcase('31547')
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=allure.testcase('31546'),
        ),
    ],
)
@pytest.mark.smoke
def test_campaign_summary_page(campaign_details_page, user):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    expect(
        campaign_details_page.page.get_by_role(
            'heading', name=AppConfigs.SAMPLE_CAMPAIGN_NAME
        )
    ).to_have_count(1)  # test title
    expect(
        campaign_details_page.page.get_by_text(AppConfigs.QA_COMPANY_NAME)
    ).to_have_count(1)


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
def test_campaign_summary_table(
    campaign_details_page: CampaignDetailsPage, user, total, field, value, record
):
    # Count the rows that do not have the text 'Preview'
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    # assert (
    #     len(campaign_details_page.table_campaign_attacks_summary.text_content())
    #     == total
    # )
    campaign_details_page.filter_employees(field, value, record)


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(), id='AW Admin', marks=allure.testcase('31550')
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=allure.testcase('31553'),
        ),
    ],
)
@pytest.mark.smoke
def test_campaign_export(campaign_details_page: CampaignDetailsPage, user):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    page_entity = CampaignAttacksSummaryFactory.get_entity(
        campaign_details_page.table_campaign_attacks_summary.text_content()[0]
    )
    if page_entity.status == 'Mail Server Error':
        page_entity.status = 'Error_Email'
    file = campaign_details_page.export_csv()
    with open(file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows: list = [row for row in reader]
    assert len(rows) == 6
    flag = False
    print('page_entity: ', page_entity)
    for i in range(len(rows)):
        csv_entity = CampaignAttacksSummaryFactory.get_entity_from_dict(rows[i])
        print('csv_entity: ', csv_entity)
        if page_entity == csv_entity:
            flag = True
            break
    assert flag


@pytest.mark.parametrize(
    'user, content_type, scenario_name',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'application/pdf',
            AppConfigs.SCENARIO_PDF_NAME,
            id='Customer Admin',
            marks=[allure.testcase('31545'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            AppConfigs.SCENARIO_DOCX_NAME,
            id='Customer Admin',
            marks=[allure.testcase('31545'), pytest.mark.xdist_group(name='agent1')],
        ),
    ],
)
@pytest.mark.smoke
def test_create_simulation_campaign_attachment(
    user: UserModel,
    employee,
    employee2,
    content_type,
    scenario_name,
    scenarios_page: ScenariosPage,
    mailtrap,
    is_staging_env,
):
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.filter.filter_by('Email', employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()

    execute_campaign_page.filter.filter_by('Email', employee2.email)

    execute_campaign_page.employee_table.get_employee_row(employee2.email).select_row()
    execute_campaign_page.review_button.click()
    assert execute_campaign_page.number_of_employees.text_content() == '2'
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()
    emails = [employee.email, employee2.email]
    filepaths = mailtrap.download_attachments_with_file_paths(
        AppConfigs.EMPLOYEE_INBOX_ID, emails, content_type, timeout=240
    )
    assert len(filepaths) == len(emails), (
        'Number of attachments does not match number of emails'
    )
    links = mailtrap.extract_links(filepaths)
    assert len(links) == len(filepaths), (
        'Number of links does not match number of attachments'
    )
    assert len(links) == len(set(links)), 'Duplicate links found'
    print('Links: ', links)
    if content_type == 'application/pdf':
        warning_page = execute_campaign_page.go_to_employee_campaign_warning_page(
            links[0] + '&constest=312'
        )
        survey_page = warning_page.go_to_survey()
        survey_page.select_radio_option(1, 1)
        survey_page.submit_survey()


@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.aw_admin(), id='AW Admin', marks=allure.testcase('31547')
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id='Customer Admin',
            marks=allure.testcase('31546'),
        ),
    ],
)
@pytest.mark.smoke
def test_campaign_target_list_change_page(
    big_campaign_details_page: CampaignDetailsPage, user
):
    if AppConfigs.ENV.startswith('development'):
        pytest.skip('Test is not ready for development env')
    assert (
        '1-15'
        in big_campaign_details_page.table_campaign_attacks_summary.get_page_count()
    )
    big_campaign_details_page.table_campaign_attacks_summary.go_to_next_page()
    assert (
        '16-30'
        in big_campaign_details_page.table_campaign_attacks_summary.get_page_count()
    )
    big_campaign_details_page.table_campaign_attacks_summary.go_to_next_page()
    assert (
        '31-45'
        in big_campaign_details_page.table_campaign_attacks_summary.get_page_count()
    )
    big_campaign_details_page.table_campaign_attacks_summary.go_to_previous_page()
    assert (
        '16-30'
        in big_campaign_details_page.table_campaign_attacks_summary.get_page_count()
    )
    big_campaign_details_page.table_campaign_attacks_summary.go_to_previous_page()
    assert (
        '1-15'
        in big_campaign_details_page.table_campaign_attacks_summary.get_page_count()
    )
