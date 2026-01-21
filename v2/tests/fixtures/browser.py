"""Browser fixtures."""
import os
import tempfile
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect


def safe_title(page: Page) -> str:
    try:
        return page.title()
    except Exception:
        return 'unknown'


@pytest.fixture
def context(request, browser: Browser, auth_state) -> Generator[BrowserContext, None, None]:
    """Browser context with shared auth and tracing."""
    if not os.getenv('BROWSER_NAME'):
        os.environ['BROWSER_NAME'] = browser.browser_type.name
        os.environ['BROWSER_VERSION'] = browser.version

    ctx = browser.new_context(
        storage_state=auth_state,
        viewport={'width': 1440, 'height': 900},
        permissions=['clipboard-read', 'clipboard-write'],
    )
    ctx.set_default_timeout(120 * 1000)
    expect.set_options(timeout=20_000)
    ctx.tracing.start(name=request.node.name, snapshots=True, screenshots=True, sources=True)

    yield ctx

    failed = getattr(request.node, 'rep_call', None) and request.node.rep_call.failed
    if failed:
        trace_path = tempfile.mktemp(prefix='trace', suffix='.zip')
        ctx.tracing.stop(path=trace_path)
        allure.attach.file(trace_path, 'trace.zip', 'application/zip')
        for pg in ctx.pages:
            allure.attach(pg.screenshot(), name=f'{safe_title(pg)}.png', attachment_type=allure.attachment_type.PNG)
    else:
        ctx.tracing.stop()

    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Fresh page per test."""
    yield context.new_page()