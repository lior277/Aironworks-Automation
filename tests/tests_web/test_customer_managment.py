import pytest
from playwright.sync_api import expect, TimeoutError
from src.page_objects.customers_page import CustomersPage
from src.models.factories.user_model_factory import UserModelFactory


@pytest.mark.parametrize(
    "user",
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
)
@pytest.mark.smoke
def test_active_customers_visible(user, sign_in_page, dashboard_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    # when logging active customers should be the visible page
    expect(dashboard_page.page.get_by_role("heading", name="Customers")).to_be_visible()

    customers_page = CustomersPage(dashboard_page.page, user)
    customers_page.validate_elements_visible()
    customers_page.validate_in_tab("active")
    customers_page.validate_active_customers_headers_are_visible()
    row = customers_page.get_customer_row()
    expect(row).to_be_visible()

    columns = row.get_by_role("cell").all()
    assert len(columns) == len(customers_page.active_customers_table_headers)


@pytest.mark.parametrize(
    "user",
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
)
@pytest.mark.smoke
def test_active_customer_spectate(user, sign_in_page, dashboard_page):
    sign_in_page.navigate(user.is_admin)
    sign_in_page.submit_sign_in_form(user)

    customers_page = CustomersPage(dashboard_page.page, user)
    expect(customers_page.page.get_by_role("progressbar")).to_have_count(0)
    row = customers_page.get_customer_row()

    expect(row).to_be_visible()

    columns = row.get_by_role("cell").all()
    company_name = columns[0].text_content()

    row.get_by_role("cell", name="Spectate").click()
    customers_page.page.wait_for_load_state(timeout=5)

    try:
        dashboard_page.page.get_by_role(
            "button", name=f"Login as admin of {company_name.lower()}"
        ).click()
        customers_page.page.wait_for_load_state(timeout=5)
    except TimeoutError:
        # this button only appears for some companies
        pass

    expect(
        dashboard_page.page.get_by_label("scrollable content").get_by_role("paragraph")
    ).to_contain_text(f"Admin of {company_name}")
