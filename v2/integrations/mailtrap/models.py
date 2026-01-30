from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MailtrapConfig(BaseModel):
    """Configuration for Mailtrap API client"""

    account_id: int = Field(..., gt=0, description='Mailtrap account ID')
    api_prefix: str = Field(
        default='/api_access', pattern='^/.*', description='API prefix path'
    )
    timeout_s: int = Field(default=30, gt=0, description='Request timeout in seconds')
    poll_interval_s: float = Field(
        default=1.0, gt=0, description='Polling interval in seconds'
    )
    max_pages: int = Field(default=5, gt=0, description='Maximum pages to fetch')

    model_config = {
        'frozen': True,  # Immutable like dataclass(frozen=True)
        'extra': 'forbid',  # Reject unknown fields
    }


class MailtrapMessageMeta(BaseModel):
    """Metadata for a Mailtrap message"""

    # Common fields from Mailtrap API
    id: int
    subject: str | None = None
    from_email: str | None = Field(default=None, alias='from_email')
    to_email: str | None = Field(default=None, alias='to_email')
    sent_at: str | None = None
    html_body_size: int | None = None
    text_body_size: int | None = None

    model_config = {
        'extra': 'allow',  # Allow extra fields from API
        'populate_by_name': True,  # Allow both 'from_email' and 'from-email'
    }


class MailtrapMessage(BaseModel):
    """A message from Mailtrap inbox"""

    inbox_id: int = Field(..., gt=0)
    id: int = Field(..., gt=0)
    meta: dict[str, Any]  # Keep flexible for now, or use MailtrapMessageMeta

    model_config = {'frozen': True, 'extra': 'forbid'}
