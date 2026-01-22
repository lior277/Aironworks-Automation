"""Browser fixtures."""

import os
import tempfile
import uuid
from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from v2.src.core.config import Config


def _safe_title(page: Page) -> str:
    try:
        return page.title()
    except Exception:
        return 'unknown'


@pytest.fixture
def context(
    request, browser: Browser, api_storage_state
) -> Generator[BrowserContext, Any, None]:
    """Browser context with auth and tracing."""
    if not os.getenv('BROWSER_NAME'):
        os.environ['BROWSER_NAME'] = browser.browser_type.name
        os.environ['BROWSER_VERSION'] = browser.version

    ctx = browser.new_context(
        storage_state=api_storage_state, viewport={'width': 1440, 'height': 900}
    )
    ctx.set_default_timeout(Config.DEFAULT_TIMEOUT * 1000)
    expect.set_options(timeout=20_000)

    ctx.tracing.start(name=request.node.name, snapshots=True, screenshots=True)

    yield ctx

    failed = getattr(request.node, 'rep_call', None) and request.node.rep_call.failed
    if failed:
        trace_path = tempfile.mktemp(prefix='trace', suffix='.zip')
        ctx.tracing.stop(path=trace_path)
        allure.attach.file(trace_path, 'trace.zip', 'application/zip')
        for pg in ctx.pages:
            allure.attach(
                pg.screenshot(),
                name=f'{_safe_title(pg)}.png',
                attachment_type=allure.attachment_type.PNG,
            )
    else:
        ctx.tracing.stop()

    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, Any, None]:
    """Fresh page per test."""
    yield context.new_page()


@pytest.fixture
def unique_id() -> str:
    """Unique ID for test data."""
    return uuid.uuid4().hex[:8]
