from dataclasses import dataclass

from playwright.sync_api import APIRequestContext, Playwright, expect


@dataclass(frozen=True)
class SendGridConfig:
    api_key: str
    from_email: str
    base_url: str = 'https://api.sendgrid.com'


class SendGridClient:
    def __init__(self, playwright: Playwright, cfg: SendGridConfig):
        self._cfg = cfg
        self._ctx: APIRequestContext = playwright.request.new_context(
            base_url=cfg.base_url,
            extra_http_headers={
                'Authorization': f'Bearer {cfg.api_key}',
                'Content-Type': 'application/json',
            },
        )

    def send_mail(self, to_email: str, subject: str, html: str) -> None:
        payload = {
            'personalizations': [{'to': [{'email': to_email}], 'subject': subject}],
            'from': {'email': self._cfg.from_email},
            'content': [{'type': 'text/html', 'value': html}],
        }
        resp = self._ctx.post('/v3/mail/send', json=payload)
        # SendGrid returns 202 on success
        expect(resp).to_be_ok()

    def close(self) -> None:
        try:
            self._ctx.dispose()
        except Exception:
            pass
