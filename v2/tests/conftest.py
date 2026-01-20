import pytest

from v2.src.core.http import ApiSession
from v2.src.core.config import Config

# Business APIs
# from v2.src.http.clients.users_api import UsersApi
# from v2.src.http.clients.campaigns_api import CampaignsApi


# =========================
# Global config validation
# =========================

@pytest.fixture(scope="session", autouse=True)
def validate_env():
    assert Config.BASE_URL, "BASE_URL is not set"
    assert Config.SERVICE_SECRET, "SERVICE_SECRET is not set"
    yield


# =========================
# Api Session (Service Auth)
# =========================

@pytest.fixture(scope="session")
def api_session():
    api = ApiSession(base_url=Config.BASE_URL)

    # Login once per session using service secret
    api.login_as_service()

    return api


# =========================
# Business API clients
# =========================

@pytest.fixture
def bonus_api(api_session):
    return BonusPageApi(api_session)


# @pytest.fixture
# def users_api(api_session):
#     return UsersApi(api_session)

# @pytest.fixture
# def campaigns_api(api_session):
#     return CampaignsApi(api_session)


# =========================
# Base URL fixture
# =========================

@pytest.fixture(scope="session")
def base_url():
    return Config.BASE_URL
