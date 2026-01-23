"""Authentication fixtures (per worker)."""

import allure
import pytest
from playwright.sync_api import Playwright, expect

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config


@pytest.fixture(scope='worker')
def api_storage_state(playwright: Playwright, tmp_path_factory) -> str:
    """Login once per worker, save cookies to storage_state."""
    worker_tmp = tmp_path_factory.mktemp('auth')
    auth_file = worker_tmp / 'auth_state.json'

    request_context = playwright.request.new_context(base_url=Config.BASE_URL)

    try:
        with allure.step('API login'):
            login_resp = request_context.post(
                AuthRoutes.LOGIN,
                data={
                    'email': Config.USER_EMAIL,
                    'password': Config.USER_PASSWORD,
                    'remember': True,
                    'otp': '',
                    'admin': False,
                },
            )
            expect(login_resp).to_be_ok()

        with allure.step('Fetch user roles'):
            info_resp = request_context.get(AuthRoutes.INFO)
            expect(info_resp).to_be_ok()
            roles = info_resp.json().get('user', {}).get('roles', [])
            assert roles, (
                f'No roles returned from {AuthRoutes.INFO}. Response: {info_resp.text()}'
            )

        with allure.step('Pick role'):
            role_id = Config.USER_ROLE_ID or roles[0]['id']
            pick_resp = request_context.post(
                AuthRoutes.PICK_ROLE, data={'role_id': role_id}
            )
            expect(pick_resp).to_be_ok()

        with allure.step('Save storage state'):
            request_context.storage_state(path=str(auth_file))

    finally:
        request_context.dispose()

    return str(auth_file)
