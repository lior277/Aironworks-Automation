"""API Client fixtures - clients receive session with auth."""
import pytest

from v2.src.api.clients.campaigns_api import CampaignsApi
from v2.src.api.clients.users_api import UsersApi
from v2.src.api.clients.employees_api import EmployeesApi


@pytest.fixture
def campaigns_api(api_session) -> CampaignsApi:
    """Campaigns API - already authenticated via api_session."""
    return CampaignsApi(api_session)


@pytest.fixture
def users_api(api_session) -> UsersApi:
    """Users API - already authenticated via api_session."""
    return UsersApi(api_session)


@pytest.fixture
def employees_api(api_session) -> EmployeesApi:
    """Employees API - already authenticated via api_session."""
    return EmployeesApi(api_session)