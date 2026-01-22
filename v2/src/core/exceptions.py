import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestContext:
    method: str
    url: str
    body: Any = None
    status_code: int = 0
    response_text: str = ''
    response_headers: dict = field(default_factory=dict)


class ApiRequestException(Exception):
    def __init__(self, request_context: RequestContext):
        self.request_context = request_context
        super().__init__(self._format_message(request_context))

    @staticmethod
    def _format_message(ctx: RequestContext) -> str:
        return (
            f'\n{"=" * 40}\nAPI REQUEST FAILED\n{"=" * 40}\n'
            f'Method: {ctx.method}\n'
            f'URL: {ctx.url}\n'
            f'Status: {ctx.status_code}\n'
            f'Request: {json.dumps(ctx.body, indent=2, ensure_ascii=False)}\n'
            f'Response: {ctx.response_text}\n'
            f'Headers: {ctx.response_headers}\n'
        )
