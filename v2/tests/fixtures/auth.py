"""Authentication fixtures (per worker)."""

import pytest
from playwright.sync_api import Playwright

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config


@pytest.fixture(scope='worker')
def api_storage_state(playwright: Playwright, tmp_path_factory) -> str:
    """Login once per worker, save cookies to storage_state."""
    worker_tmp = tmp_path_factory.mktemp('auth')
    auth_file = worker_tmp / 'auth_state.json'

    request_context = playwright.request.new_context(base_url=Config.BASE_URL)

    try:
        # Login
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
        assert login_resp.ok, f'Login failed: {login_resp.status}'

        # Get roles
        info_resp = request_context.get(AuthRoutes.INFO)
        assert info_resp.ok, f'Info failed: {info_resp.status}'
        roles = info_resp.json().get('user', {}).get('roles', [])
        assert roles, 'No roles returned from /api/auth/info'

        # Pick role
        role_id = Config.USER_ROLE_ID or roles[0]['id']
        pick_resp = request_context.post(
            AuthRoutes.PICK_ROLE, data={'role_id': role_id}
        )
        assert pick_resp.ok, f'Pick role failed: {pick_resp.status}'

        # Save cookies
        request_context.storage_state(path=str(auth_file))

    finally:
        request_context.dispose()

    return str(auth_file)
