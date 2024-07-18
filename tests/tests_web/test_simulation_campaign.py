import csv
import re

import pytest
from playwright.sync_api import expect

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.campaign_detalis_page import CampaignDetailsPage
from src.page_objects.entity.campaign_attacks_summary_entity import CampaignAttacksSummaryFactory
from src.page_objects.scenarios_page import ScenariosPage
from src.utils.mailtrap import find_email


@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), id="AW Admin",
                                               marks=pytest.mark.test_id("C31544")),
                                  pytest.param(UserModelFactory.customer_admin(), id="Customer Admin",
                                               marks=pytest.mark.test_id("C31545"))])
@pytest.mark.smoke
def test_create_simulation_campaign(user: UserModel, employee, scenarios_page: ScenariosPage, mailtrap):
    scenario_name = AppConfigs.EXAMPLE_SCENARIO_NAME
    scenarios_page.filter_by_name(scenario_name)
    generic_scenario = scenarios_page.find_scenario(scenario_name)

    generic_scenario.click()

    execute_campaign_page = scenarios_page.execute_scenario()
    if user.is_admin:
        execute_campaign_page.pick_company(AppConfigs.QA_COMPANY_NAME)
    execute_campaign_page.pick_employees.click()
    expect(execute_campaign_page.employee_table.table).to_be_visible()
    execute_campaign_page.employee_table.set_filter_column("email", employee.email)

    execute_campaign_page.employee_table.get_employee_row(employee.email).select_row()
    execute_campaign_page.review_button.click()
    execute_campaign_page.execute_button.click()
    execute_campaign_page.confirm_execute_button.click()

    mail = mailtrap.wait_for_mail(AppConfigs.EMPLOYEE_INBOX_ID, find_email(employee.email), timeout=240)

    assert mail is not None


@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(),
                                               id="AW Admin", marks=pytest.mark.test_id("C31547")),
                                  pytest.param(UserModelFactory.customer_admin(),
                                               id="Customer Admin", marks=pytest.mark.test_id("C31546"))])
@pytest.mark.smoke
def test_campaigns_page_has_data(user, campaigns_page):
    tables = campaigns_page.page.get_by_test_id("executions-table")
    expect(tables).to_have_count(2)
    expect(campaigns_page.page.get_by_role("progressbar")).to_have_count(0)
    tables = tables.all()
    assert tables[0].get_by_role("row").count() >= 2
    assert tables[1].get_by_role("row").count() >= 2


@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(),
                                               id="AW Admin", marks=pytest.mark.test_id("C31547"), ),
                                  pytest.param(UserModelFactory.customer_admin(), id="Customer Admin",
                                               marks=pytest.mark.test_id("C31546"))])
@pytest.mark.smoke
def test_campaign_summary_page(campaign_details_page, user):
    expect(campaign_details_page.page.get_by_role(
        "heading", name=re.compile(AppConfigs.SAMPLE_CAMPAIGN_NAME + ".*"))).to_have_count(1)  # test title
    expect(campaign_details_page.page.get_by_text("1 days")).to_have_count(1)  # test duration
    expect(campaign_details_page.page.get_by_text(AppConfigs.QA_COMPANY_NAME)).to_have_count(1)


@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(), id="AW Admin",
                                               marks=pytest.mark.test_id("C31549")),
                                  pytest.param(UserModelFactory.customer_admin(), id="Customer Admin",
                                               marks=pytest.mark.test_id("C31552"))])
@pytest.mark.smoke
def test_campaign_summary_table(campaign_details_page: CampaignDetailsPage, user):
    expect(campaign_details_page.page.get_by_role("row").and_(
        campaign_details_page.page.locator("[role='row']", has_not_text="Preview"))).to_have_count(2)


@pytest.mark.parametrize("user", [pytest.param(UserModelFactory.aw_admin(),
                                               id="AW Admin", marks=pytest.mark.test_id("C31550")),
                                  pytest.param(UserModelFactory.customer_admin(),
                                               id="Customer Admin",
                                               marks=pytest.mark.test_id("C31553"))])
@pytest.mark.smoke
def test_campaign_export(campaign_details_page: CampaignDetailsPage, user):
    page_entity = CampaignAttacksSummaryFactory.get_entity(
        campaign_details_page.table_campaign_attacks_summary.text_content()[0])

    file = campaign_details_page.export_csv()
    with open(file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows: list = [row for row in reader]
    assert len(rows) == 1
    csv_entity = CampaignAttacksSummaryFactory.get_entity_from_dict(rows[0])

    assert page_entity == csv_entity
