import pytest
import re
import csv
from playwright.sync_api import expect
from src.models.factories.user_model_factory import UserModelFactory
from src.configs.config_loader import AppConfigs
from src.utils.mailtrap import find_email
from src.page_objects.campaign_detalis_page import CampaignDetailsPage


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31544"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31545"),
        ),
    ],
)
def test_create_simulation_campaign(user, employee, sign_in_page, mailtrap):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    scenarios_page = sign_in_page.navigation_bar.navigate_scenarios()
    scenario_name = "General Scenario - English"
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

    mail = mailtrap.wait_for_mail(
        AppConfigs.EMPLOYEE_INBOX_ID,
        find_email(
            employee.email,
        ),
        timeout=240,
    )

    assert mail is not None


@pytest.mark.parametrize(
    "user",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31547"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31546"),
        ),
    ],
)
def test_campaigns_page_has_data(user, sign_in_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    campaigns_page = sign_in_page.navigation_bar.navigate_campaigns()
    tables = campaigns_page.page.get_by_test_id("executions-table")
    expect(tables).to_have_count(2)
    expect(campaigns_page.page.get_by_role("progressbar")).to_have_count(0)
    tables = tables.all()
    assert tables[0].get_by_role("row").count() >= 2
    assert tables[1].get_by_role("row").count() >= 2


@pytest.fixture
def campaign_details_page(request, sign_in_page) -> CampaignDetailsPage:
    user = request.param
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)
    expect(
        sign_in_page.page.get_by_role("link", name="Settings")
    ).to_be_visible()  # wait for login to finish before navigating
    sign_in_page.page.goto(
        (AppConfigs.ADMIN_BASE_URL if user.is_admin else AppConfigs.BASE_URL)
        + "admin/dashboard/attacks/executions/"
        + AppConfigs.SAMPLE_CAMPAIGN
    )

    return CampaignDetailsPage(sign_in_page.page)


@pytest.mark.parametrize(
    "campaign_details_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31547"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31546"),
        ),
    ],
    indirect=["campaign_details_page"],
)
def test_campaign_summary_page(campaign_details_page, sign_in_page):
    expect(
        campaign_details_page.page.get_by_role(
            "heading", name=re.compile("Scenario - Test AW Admin.*")
        )
    ).to_have_count(1)  # test title
    expect(campaign_details_page.page.get_by_text("1 days")).to_have_count(
        1
    )  # test duration
    expect(
        campaign_details_page.page.get_by_text(AppConfigs.QA_COMPANY_NAME)
    ).to_have_count(1)  # test company name in page


@pytest.mark.parametrize(
    "campaign_details_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31549"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31552"),
        ),
    ],
    indirect=["campaign_details_page"],
)
def test_campaign_summary_table(campaign_details_page: CampaignDetailsPage):
    expect(campaign_details_page.page.get_by_role("row")).to_have_count(2)


@pytest.mark.parametrize(
    "campaign_details_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="AW Admin",
            marks=pytest.mark.test_id("C31550"),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            id="Customer Admin",
            marks=pytest.mark.test_id("C31553"),
        ),
    ],
    indirect=["campaign_details_page"],
)
def test_campaign_export(campaign_details_page: CampaignDetailsPage):
    file = campaign_details_page.export_csv()
    with open(file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader]
    assert len(rows) == 1
    del rows[0]["Failure Date"]
    assert rows[0] == {
        "Device": "Generic Feature Phone / Debian / Other",
        "Email": "fae1336c2d-da5a02+cjnksfoqlnbhxacrwgfk@inbox.mailtrap.io",
        "First Name": "Janice",
        "IP Address": "34.73.195.161",
        "Last Name": "Bailey",
        "Report Date": "",
        "Status": "SUCCESSFUL",
    }
