import re
import time

import pytest
from playwright.sync_api import expect, TimeoutError

from src.apis.api_factory import api
from src.apis.utils import get_request_context_for_page
from src.configs.config_loader import AppConfigs
from src.models.factories.auth.signup_model_factory import SignupModelFactory
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.customers_page import CustomersPage


@pytest.fixture
def customers_page(request, sign_in_page, dashboard_page):
    user = request.param
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    customers_page = CustomersPage(dashboard_page.page, user)
    expect(customers_page.page.get_by_role("progressbar")).to_have_count(0)

    return customers_page


@pytest.mark.parametrize(
    "customers_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="active customers visible",
            marks=pytest.mark.test_id("C31499"),
        ),
        pytest.param(
            UserModelFactory.reseller_admin(),
            id="active customers visible for reseller admin",
            marks=pytest.mark.test_id("C31500"),
        ),
    ],
    indirect=["customers_page"],
)
@pytest.mark.smoke
def test_active_customers_visible(customers_page, dashboard_page):
    # when logging active customers should be the visible page
    expect(dashboard_page.page.get_by_role("heading", name="Customers")).to_be_visible()

    customers_page.validate_elements_visible()
    customers_page.validate_in_tab("active")
    customers_page.validate_active_customers_headers_are_visible()
    row = customers_page.get_customer_row()
    expect(row).to_be_visible()

    columns = row.get_by_role("cell").all()
    assert len(columns) == len(customers_page.active_customers_table_headers)


@pytest.mark.parametrize(
    "customers_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="customer can be spectated",
            marks=pytest.mark.test_id("C31502"),
        ),
        pytest.param(
            UserModelFactory.reseller_admin(),
            id="customer can be spectated as reseller admin",
            marks=pytest.mark.test_id("C31501"),
        ),
    ],
    indirect=["customers_page"],
)
@pytest.mark.smoke
def test_active_customer_spectate(customers_page, dashboard_page):
    row = customers_page.get_customer_row()

    expect(row).to_be_visible()

    columns = row.get_by_role("cell").all()
    company_name = columns[0].text_content()

    row.get_by_role("cell", name="Spectate").click()
    customers_page.page.wait_for_load_state(timeout=5)

    try:
        dashboard_page.page.get_by_role(
            "button", name=f"Login as admin of {company_name.lower()}"
        ).click(timeout=500)
        customers_page.page.wait_for_load_state(timeout=5)
    except TimeoutError:
        # this button only appears for some companies
        pass

    expect(
        dashboard_page.page.get_by_label("scrollable content").get_by_role("paragraph")
    ).to_contain_text(f"Admin of {company_name}")


@pytest.mark.parametrize(
    "customers_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="new customer count is correct for aw admin",
            marks=pytest.mark.test_id("C31503"),
        ),
        pytest.param(
            UserModelFactory.reseller_admin(),
            id="new customer count is correct for reseller admin",
            marks=pytest.mark.test_id("C31504"),
        ),
    ],
    indirect=["customers_page"],
)
@pytest.mark.smoke
def test_new_customers_count(customers_page: CustomersPage, playwright):
    expect(customers_page.page.get_by_test_id("empty-state")).not_to_be_visible()
    request_context = get_request_context_for_page(
        playwright, customers_page.page, AppConfigs.ADMIN_BASE_URL
    )
    admin_service = api.admin(request_context)
    company_counts = admin_service.company_count()
    expect(company_counts).to_be_ok()

    new_count = company_counts.json()["new"]
    content = customers_page.tabs["new"].text_content()

    match = re.compile(f"New Customers.*({new_count})", re.IGNORECASE).match(content)
    assert match is not None, f"{content=}"

    assert abs(int(match.group(1)) - new_count) < 2


@pytest.mark.parametrize(
    "customers_page",
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            id="aw admin can approve new customer",
            marks=pytest.mark.test_id("C31505"),
        ),
        pytest.param(
            UserModelFactory.reseller_admin(),
            id="reseller admin can approve new customer",
            marks=pytest.mark.test_id("C31506"),
        ),
    ],
    indirect=["customers_page"],
)
@pytest.mark.smoke
def test_approve_new_customer(customers_page, sign_in_page, dashboard_page, playwright, api_request_context_aw_admin):
    referral = None
    if customers_page.user.is_reseller:
        signed_in_context = get_request_context_for_page(
            playwright, sign_in_page.page, AppConfigs.ADMIN_BASE_URL
        )
        info = api.login(signed_in_context).info()
        expect(info).to_be_ok()
        referral = info.json()["user"]["reseller_company_id"]

    context = playwright.request.new_context(base_url=AppConfigs.BASE_URL)

    new_customer = SignupModelFactory.random_customer(referral=referral)
    expect(api.login(context).register(new_customer)).to_be_ok()

    customers_page.tabs["new"].click()
    customer_row = customers_page.page.get_by_role("row").filter(
        has_text=new_customer.company_name
    )
    customer_row.get_by_role("button", name="Approve").click()
    customers_page.page.get_by_role("button", name="Confirm Approval").click()

    time.sleep(1)
    tries = 0
    admin_service = api.admin(api_request_context_aw_admin)
    while True and tries < 10:
        companies = admin_service.get_companies_list(type="active")
        expect(companies).to_be_ok()
        companies = companies.json()
        company = next(
            (c for c in companies["items"] if c["name"] == new_customer.company_name),
            None,
        )
        if company is None:
            time.sleep(1)
            tries += 1
            continue
        admin_service.deactivate_company(company["id"])


@pytest.mark.parametrize(
    "customers_page",
    [
        pytest.param(
            UserModelFactory.reseller_admin(),
            id="reseller admin can approve new customer",
            marks=pytest.mark.test_id("C31507"),
        ),
    ],
    indirect=["customers_page"],
)
@pytest.mark.smoke
def test_copy_invitation_link(customers_page, sign_in_page, playwright):
    signed_in_context = get_request_context_for_page(playwright, sign_in_page.page, AppConfigs.ADMIN_BASE_URL)

    info = api.login(signed_in_context).info()
    expect(info).to_be_ok()
    referral = info.json()["user"]["reseller_company_id"]

    customers_page.copy_invitation_link_button.click()
    expect(
        customers_page.page.get_by_text("Invite link copied to clipboard.")
    ).to_be_visible()
    clipboard_text = customers_page.page.evaluate("navigator.clipboard.readText()")

    assert referral in clipboard_text
