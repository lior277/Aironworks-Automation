from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from v2.src.api.api_routes.auth_routes import AuthRoutes
from v2.src.api.models.auth import LoginRequest, PickRoleRequest, UserInfo
from v2.src.core.config import Config

if TYPE_CHECKING:
    from v2.src.core.http.api_session import ApiSession


class AuthService:
    """Handles authentication flow during fixture setup (NOT in tests)."""

    def __init__(
        self,
        api_session: ApiSession,
        login_request: LoginRequest,
        role_id: str | None = None,
    ):
        self.api = api_session
        self.login_request = login_request
        self.role_id = role_id

    def login_and_save_state(self, storage_state_path: Path) -> None:
        self._ensure_parent_dir(storage_state_path)
        self._login()
        self._assert_refresh_cookie_present()
        user_info = self._get_user_info()
        self._pick_role(user_info)
        self._save_state(storage_state_path)

    @staticmethod
    def _ensure_parent_dir(path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

    def _login(self) -> None:
        # Keep existing behavior: send form data
        self.api.post(AuthRoutes.LOGIN, data=self.login_request.to_dict())

    def _assert_refresh_cookie_present(self) -> None:
        state = self.api.storage_state()
        cookie_names = {c.get('name') for c in state.get('cookies', [])}
        if 'refresh_token' not in cookie_names:
            raise RuntimeError(
                f'Login did not create refresh_token cookie. cookies={sorted(x for x in cookie_names if x)}'
            )

    def _get_user_info(self) -> UserInfo:
        return UserInfo(self.api.get(AuthRoutes.INFO).json())

    def _pick_role(self, user_info: UserInfo) -> None:
        role_id = (
            self.role_id or Config.CUSTOMER_ROLE_ID or user_info.get_first_role_id()
        )
        self.api.post(AuthRoutes.PICK_ROLE, data=PickRoleRequest(role_id).to_dict())

    def _save_state(self, storage_state_path: Path) -> None:
        self.api.save_storage_state(storage_state_path)
