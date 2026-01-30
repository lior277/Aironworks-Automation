import os

import pytest
from playwright.sync_api import Page

from v2.src.core.config import Config


@pytest.mark.parametrize('test_num', range(10))
def test_worker_isolation(test_num: int, page: Page, worker_id: str):
    print(f'\nTest {test_num} running on worker: {worker_id}')
    print(f'Process ID: {os.getpid()}')

    page.goto(f'{Config.APP_BASE_URL}/admin/dashboard/attacks/executions')
    assert '/login' not in page.url.lower()
