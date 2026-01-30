# v2/tests/test_auth_state_skips_login_and_refresh_works.py
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, Playwright

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.core.config import Config
from v2.src.core.http.api_session import ApiSession


@allure.feature('Authentication')
@allure.story('Cached Auth State')
@allure.severity(allure.severity_level.CRITICAL)
def test_auth_state_skips_login(page: Page, auth_state_file: str):  # ✅ FIXED
    """Verify UI skips login flow when using cached auth state."""
    resp = page.goto(
        f'{Config.APP_BASE_URL}/admin/dashboard/attacks/executions',
        wait_until='domcontentloaded',
    )
    assert resp is not None and resp.ok, (
        f'UI navigation failed: {resp.status if resp else "no response"}'
    )
    assert '/login' not in page.url.lower(), f'Redirected to login: {page.url}'


@allure.feature('Authentication')
@allure.story('Cached Auth State')
@allure.severity(allure.severity_level.CRITICAL)
def test_api_uses_cached_auth_state(playwright: Playwright, auth_state_file: str):
    """Verify API requests work without login when using cached auth state."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        r = s.get(AuthRoutes.INFO)
        assert r.status == 200, f'/info expected 200, got {r.status}'
    finally:
        s.close()


@allure.feature('Authentication')
@allure.story('Token Refresh')
@allure.severity(allure.severity_level.CRITICAL)
def test_refresh_endpoint_works_for_api(playwright: Playwright, auth_state_file: str):
    """Verify refresh endpoint issues new tokens and API requests continue to work."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        state_before = s.storage_state()
        cookies_before = {
            c.get('name'): c.get('value') for c in state_before.get('cookies', [])
        }
        token_before = cookies_before.get('token')

        resp = s.post(AuthRoutes.REFRESH_TOKEN)
        assert resp.status == 200, f'Refresh failed: {resp.status}'

        state_after = s.storage_state()
        cookies_after = {
            c.get('name'): c.get('value') for c in state_after.get('cookies', [])
        }
        token_after = cookies_after.get('token')

        assert token_after is not None, 'Token missing after refresh'
        assert token_after != token_before, 'Token should change after refresh'

        attack_info_resp = s.get(
            '/api/admin/get_attack_info',
            params={'id': '6d2553281a76465d9271969f85cb155e'},
        )
        assert attack_info_resp.status == 200, (
            f'API call after refresh expected 200, got {attack_info_resp.status}'
        )
    finally:
        s.close()


@allure.feature('Authentication')
@allure.story('Token Refresh')
@allure.severity(allure.severity_level.CRITICAL)
def test_refresh_endpoint_works_for_ui(
    page: Page,  # ✅ FIXED
    playwright: Playwright,
    auth_state_file: str,
):
    """Verify refresh endpoint issues new tokens and UI navigation continues to work."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        resp = s.post(AuthRoutes.REFRESH_TOKEN)
        assert resp.status == 200, f'Refresh failed: {resp.status}'

        # Persist rotated cookies for the worker cache
        s.save_storage_state(auth_state_file)

        nav_resp = page.goto(
            f'{Config.APP_BASE_URL}/admin/dashboard/attacks/create'
            f'?clone=6d2553281a76465d9271969f85cb155e',
            wait_until='domcontentloaded',
        )
        assert nav_resp is not None and nav_resp.ok, (
            f'UI navigation after refresh failed: {nav_resp.status if nav_resp else "no response"}'
        )
        assert '/login' not in page.url.lower(), (
            f'Redirected to login after refresh: {page.url}'
        )
    finally:
        s.close()


# ---------------------------
# Demo / training tests
# ---------------------------


@allure.feature('Authentication')
@allure.story('Test Control')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skip(reason='Example test to demonstrate skip status in Allure report')
def test_skip_example():
    assert True


@allure.feature('Authentication')
@allure.story('Test Control')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(Config.ENV == 'production', reason='Skip in production environment')
def test_conditional_skip():
    assert Config.ENV != 'production'


@allure.feature('Authentication')
@allure.story('Error Examples')
@allure.severity(allure.severity_level.MINOR)
def test_assertion_failure_example(playwright: Playwright, auth_state_file: str):
    """Intentional failure for Allure demo."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        r = s.get(AuthRoutes.INFO)
        assert r.status == 404, 'Intentional failure for demonstration'
    finally:
        s.close()


@allure.feature('Authentication')
@allure.story('Error Examples')
@allure.severity(allure.severity_level.MINOR)
def test_exception_example(playwright: Playwright, auth_state_file: str):
    """Intentional error for Allure demo."""
    s = ApiSession(
        playwright, base_url=Config.APP_BASE_URL, storage_state=auth_state_file
    )
    try:
        response_data = s.get(AuthRoutes.INFO).json()
        _ = response_data['invalid_key']  # raises KeyError
    finally:
        s.close()


def test_ui_failure_example(page: Page):  # ✅ FIXED
    """Intentional UI failure to demonstrate trace.zip in Allure."""
    page.goto(f'{Config.APP_BASE_URL}/admin/dashboard/attacks/executions')
    assert '/nonexistent' in page.url, f'Intentional failure, got URL: {page.url}'
