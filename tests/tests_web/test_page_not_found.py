import uuid

import allure
import pytest
from playwright.sync_api import expect

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.dashboard_page import DashboardPage
from tests.tests_web import (
    browser_title,
    page_not_found_description,
    page_not_found_title,
)


@pytest.mark.parametrize(
    'user,url',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/groups/edit/id',
            id='Groups edit',
            marks=allure.testcase('31715'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/groups/view/id',
            id='Groups view',
            marks=allure.testcase('31716'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/active/edit/id',
            id='Employee edit',
            marks=allure.testcase('31717'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/admins/edit/id',
            id='Admin edit',
            marks=allure.testcase('31718'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/group-admins/edit/id',
            id='Group admin edit',
            marks=allure.testcase('31719'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/customers/edit/id',
            id='Customers edit as AW admin',
            marks=allure.testcase('31720'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/resellers/id',
            id='Resellers view',
            marks=allure.testcase('31721'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/scenario-requests/view/id',
            id='Scenario requests view as AW admin',
            marks=allure.testcase('31722'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/content-library/id',
            id='Content library view',
            marks=allure.testcase('31723'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/content-library/id',
            id='Content library view as AW admin',
            marks=allure.testcase('31724'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/education-campaigns/view/id',
            id='Education campaigns view',
            marks=allure.testcase('31725'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/education-campaigns/view/id',
            id='Education campaigns view as AW admin',
            marks=allure.testcase('31726'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/attacks/scenario-requests/view/id',
            id='Scenario requests view',
            marks=allure.testcase('31727'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/attacks/executions/id',
            id='Executions view',
            marks=allure.testcase('31728'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/attacks/executions/id',
            id='Executions view as AW admin',
            marks=allure.testcase('31729'),
        ),
    ],
)
@pytest.mark.smoke
def test_page_not_found(user: UserModel, dashboard_page: DashboardPage, url: str):
    dashboard_page.page.goto(
        url=dashboard_page.default_url + url.format(id=str(uuid.uuid4()))
    )
    expect(dashboard_page.back_home_button).to_be_visible()
    expect(dashboard_page.page).to_have_title(browser_title)
    expect(dashboard_page.page.get_by_text(page_not_found_title)).to_be_visible()
    expect(dashboard_page.page.get_by_text(page_not_found_description)).to_be_visible()
