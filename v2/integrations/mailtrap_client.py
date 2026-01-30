from __future__ import annotations

import os
import tempfile
import time
from email import message_from_bytes
from email.message import Message
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Sequence

from v2.integrations.mailtrap.models import MailtrapConfig, MailtrapMessage
from v2.src.core.config import Config
from v2.src.core.http.api_session import ApiSession


class MailtrapError(RuntimeError):
    pass


class MailtrapClient:
    def __init__(self, api: ApiSession, cfg: MailtrapConfig) -> None:
        self._api = api
        self._cfg = cfg

    def _path(self, inbox_id: int, suffix: str) -> str:
        prefix = self._cfg.api_prefix.rstrip('/')
        return f'{prefix}/accounts/{self._cfg.account_id}/inboxes/{inbox_id}{suffix}'

    def list_messages(
        self, inbox_id: int, *, search: str | None = None, page: int | None = None
    ) -> list[dict[str, Any]]:
        resp = self._api.get(
            self._path(inbox_id, '/messages'), params={'search': search, 'page': page}
        )
        return resp.json()

    def inbox_attributes(self, inbox_id: int) -> dict[str, Any]:
        return self._api.get(self._path(inbox_id, '')).json()

    def delete_message(self, inbox_id: int, message_id: int) -> None:
        self._api.delete(self._path(inbox_id, f'/messages/{message_id}'))

    def clean_inbox(self, inbox_id: int) -> None:
        self._api.patch(self._path(inbox_id, '/clean'))

    def body(
        self,
        inbox_id: int,
        message_id: int,
        kind: Literal['txt', 'htmlsource', 'raw', 'eml'],
    ) -> str | bytes:
        suffix = {
            'txt': '/body.txt',
            'htmlsource': '/body.htmlsource',
            'raw': '/body.raw',
            'eml': '/body.eml',
        }[kind]
        resp = self._api.get(self._path(inbox_id, f'/messages/{message_id}{suffix}'))
        return resp.body() if kind in ('raw', 'eml') else resp.text()

    def mail_headers(self, inbox_id: int, message_id: int) -> dict[str, Any]:
        return self._api.get(
            self._path(inbox_id, f'/messages/{message_id}/mail_headers')
        ).json()

    def iter_messages(
        self,
        inbox_id: int,
        *,
        search: str | None = None,
        start_after_id: int | None = None,
        max_pages: int | None = None,
    ) -> Iterable[dict[str, Any]]:
        pages = max_pages or self._cfg.max_pages
        for page in range(1, pages + 1):
            batch = self.list_messages(inbox_id, search=search, page=page)
            if not batch:
                return
            for m in batch:
                mid = int(m.get('id', 0))
                if start_after_id is not None and mid <= start_after_id:
                    continue
                yield m

    def latest_message_id(
        self, inbox_id: int, *, search: str | None = None
    ) -> int | None:
        msgs = self.list_messages(inbox_id, search=search, page=1)
        if not msgs:
            return None
        return max(int(m['id']) for m in msgs if 'id' in m)

    def wait_for_message(
        self,
        inbox_id: int,
        *,
        search: str | None = None,
        match: Callable[[dict[str, Any]], bool] | None = None,
        timeout_s: int | None = None,
        poll_interval_s: float | None = None,
        ignore_existing: bool = True,
    ) -> MailtrapMessage:
        timeout_s = timeout_s or self._cfg.timeout_s
        poll_interval_s = poll_interval_s or self._cfg.poll_interval_s

        start_after_id = (
            self.latest_message_id(inbox_id, search=search) if ignore_existing else None
        )
        deadline = time.monotonic() + timeout_s

        while time.monotonic() < deadline:
            for m in self.iter_messages(
                inbox_id, search=search, start_after_id=start_after_id
            ):
                if match is None or match(m):
                    return MailtrapMessage(inbox_id=inbox_id, id=int(m['id']), meta=m)
            time.sleep(poll_interval_s)

        raise TimeoutError(
            f'Mail not received within {timeout_s}s (inbox_id={inbox_id}, search={search!r}).'
        )

    def download_attachments(
        self,
        inbox_id: int,
        message_id: int,
        *,
        content_types: Sequence[str] | None = None,
        output_dir: Path | None = None,
    ) -> list[Path]:
        raw = self.body(inbox_id, message_id, 'raw')
        assert isinstance(raw, (bytes, bytearray))

        msg: Message = message_from_bytes(raw)
        output_dir = output_dir or Path(tempfile.mkdtemp(prefix='mailtrap_'))
        saved: list[Path] = []

        for part in msg.walk():
            filename = part.get_filename()
            if not filename:
                continue

            ctype = part.get_content_type()
            if content_types and ctype not in content_types:
                continue

            payload = part.get_payload(decode=True)
            if not payload:
                continue

            target = output_dir / os.path.basename(filename)
            target.write_bytes(payload)
            saved.append(target)

        return saved


def build_mailtrap_client(mailtrap_api_session: ApiSession) -> MailtrapClient:
    if not Config.MAILTRAP_API_TOKEN or int(Config.MAILTRAP_ACCOUNT_ID) <= 0:
        raise MailtrapError('MAILTRAP_API_TOKEN / MAILTRAP_ACCOUNT_ID are missing')

    cfg = MailtrapConfig(
        account_id=int(Config.MAILTRAP_ACCOUNT_ID),
        api_prefix=Config.MAILTRAP_API_PREFIX or '/api',  # fallback
        timeout_s=Config.MAILTRAP_TIMEOUT_SEC,
        poll_interval_s=Config.MAILTRAP_POLL_INTERVAL_SEC,
        max_pages=Config.MAILTRAP_MAX_PAGES,
    )
    return MailtrapClient(api=mailtrap_api_session, cfg=cfg)
