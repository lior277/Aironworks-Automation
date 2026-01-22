"""Campaign domain models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Campaign:
    id: str
    name: str
    description: str | None = None
    status: str | None = None
    raw: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Campaign':
        # Try common keys seen in many APIs
        cid = str(data.get('id') or data.get('_id') or data.get('campaign_id') or '')
        name = str(data.get('name') or data.get('campaignName') or '')
        if not cid or not name:
            # Keep raw for debugging
            raise ValueError(f'Campaign dict missing id/name: {data}')
        return cls(
            id=cid,
            name=name,
            description=data.get('description'),
            status=data.get('status') or data.get('state'),
            raw=data,
        )
