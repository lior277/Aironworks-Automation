import uuid

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
            marks=pytest.mark.test_id('C31715'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/groups/view/id',
            marks=pytest.mark.test_id('C31716'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/active/edit/id',
            marks=pytest.mark.test_id('C31717'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/admins/edit/id',
            marks=pytest.mark.test_id('C31718'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'dashboard/company/employees/group-admins/edit/id',
            marks=pytest.mark.test_id('C31719'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/customers/edit/id',
            marks=pytest.mark.test_id('C31720'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/resellers/id',
            marks=pytest.mark.test_id('C31721'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/scenario-requests/view/id',
            marks=pytest.mark.test_id('C31722'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/content-library/id',
            marks=pytest.mark.test_id('C31723'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/content-library/id',
            marks=pytest.mark.test_id('C31724'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/education-campaigns/view/id',
            marks=pytest.mark.test_id('C31725'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/education-campaigns/view/id',
            marks=pytest.mark.test_id('C31726'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/attacks/scenario-requests/view/id',
            marks=pytest.mark.test_id('C31727'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'admin/dashboard/attacks/executions/id',
            marks=pytest.mark.test_id('C31728'),
        ),
        pytest.param(
            UserModelFactory.aw_admin(),
            'admin/dashboard/attacks/executions/id',
            marks=pytest.mark.test_id('C31729'),
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
