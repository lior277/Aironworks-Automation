"""
Custom exceptions and error context models for API automation.
"""

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestContext:
    """Encapsulates request/response data for error reporting."""

    method: str
    url: str
    body: Any = None
    status_code: int = 0
    response_text: str = ''
    response_headers: dict = field(default_factory=dict)


class ApiRequestException(Exception):
    """Raised when API returns non-2xx status."""

    def __init__(self, request_context: RequestContext):
        self.request_context = request_context
        super().__init__(self._format_message(request_context))

    @property
    def status_code(self) -> int:
        """Quick access to status code."""
        return self.request_context.status_code

    @property
    def response_json(self) -> dict | None:
        """Try to parse response as JSON."""
        try:
            return json.loads(self.request_context.response_text)
        except (json.JSONDecodeError, TypeError):
            return None

    @staticmethod
    def _format_message(request_context: RequestContext) -> str:
        return (
            f'\n{"=" * 40}\n'
            f'API REQUEST FAILED\n'
            f'{"=" * 40}\n'
            f'Method: {request_context.method}\n'
            f'URL: {request_context.url}\n'
            f'Status: {request_context.status_code}\n'
            f'Request: {to_json(request_context.body)}\n'
            f'Response: {request_context.response_text}\n'
            f'Headers: {request_context.response_headers}\n'
        )


def to_json(obj: Any) -> str:
    """Safe JSON serialization."""
    try:
        return json.dumps(obj, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(obj)
