"""Playwright tracing utilities."""

import tempfile

import allure
from playwright.sync_api import BrowserContext, Page


class TracingManager:
    """Manage Playwright tracing."""

    def __init__(self, context: BrowserContext, test_name: str):
        self.context = context
        self.test_name = test_name

    def start(self) -> None:
        """Start tracing."""
        self.context.tracing.start(
            name=self.test_name, snapshots=True, screenshots=True, sources=True
        )

    def stop(self, failed: bool = False) -> None:
        """Stop tracing, save if failed."""
        if failed:
            trace_path = tempfile.mktemp(prefix='trace', suffix='.zip')
            self.context.tracing.stop(path=trace_path)
            allure.attach.file(trace_path, 'trace.zip', 'application/zip')
            self._attach_screenshots()
        else:
            self.context.tracing.stop()

    def _attach_screenshots(self) -> None:
        """Attach screenshots of all pages."""
        for page in self.context.pages:
            title = self._safe_title(page)
            allure.attach(
                page.screenshot(),
                name=f'{title}.png',
                attachment_type=allure.attachment_type.PNG,
            )

    @staticmethod
    def _safe_title(page: Page) -> str:
        try:
            return page.title() or 'untitled'
        except Exception:
            return 'unknown'
