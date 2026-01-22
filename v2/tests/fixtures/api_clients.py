"""API Client fixtures using Playwright API."""

import pytest

from v2.src.api.clients.education_api import EducationApi
from v2.src.api.clients.employees_api import EmployeesApi
from v2.src.api.clients.groups_api import GroupsApi
from v2.src.api.clients.scenarios_api import ScenariosApi
from v2.src.pages.api_pages.campaigns_api import CampaignsApi


@pytest.fixture(scope='session')
def campaigns_api(api_context) -> CampaignsApi:
    """Campaigns API client."""
    return CampaignsApi(api_context)


@pytest.fixture(scope='session')
def employees_api(api_context) -> EmployeesApi:
    """Employees API client."""
    return EmployeesApi(api_context)


@pytest.fixture(scope='session')
def groups_api(api_context) -> GroupsApi:
    """Groups API client."""
    return GroupsApi(api_context)


@pytest.fixture(scope='session')
def scenarios_api(api_context) -> ScenariosApi:
    """Scenarios API client."""
    return ScenariosApi(api_context)


@pytest.fixture(scope='session')
def education_api(api_context) -> EducationApi:
    """Education API client."""
    return EducationApi(api_context)
