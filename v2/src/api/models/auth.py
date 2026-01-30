from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class _DictMixin:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)  # type: ignore[return-value]


@dataclass(frozen=True)
class LoginRequest(_DictMixin):
    email: str
    password: str
    remember: bool = True
    otp: str = ''
    admin: bool = False


@dataclass(frozen=True)
class PickRoleRequest(_DictMixin):
    role_id: str


@dataclass(frozen=True)
class UserInfo:
    raw: dict[str, Any]

    def get_first_role_id(self) -> str:
        roles = self.raw.get('user', {}).get('roles') or self.raw.get('roles', [])
        for role in roles:
            role_id = role.get('id') or role.get('role_id')
            if role_id:
                return str(role_id)
        raise ValueError(f'No roles found in: {self.raw}')
