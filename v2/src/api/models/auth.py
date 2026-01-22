"""
Authentication models.
"""

from dataclasses import dataclass


@dataclass
class LoginData:
    """Request payload for service login."""

    service_secret: str


@dataclass
class LoginResponse:
    """Response from service login."""

    access_token: str

    @classmethod
    def from_dict(cls, data: dict) -> 'LoginResponse':
        token = data.get('access_token')
        if not token:
            raise ValueError('Login response missing access_token')
        return cls(access_token=token)
