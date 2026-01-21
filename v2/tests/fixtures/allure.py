"""Allure reporting fixtures."""

from pathlib import Path

import pytest

from v2.src.core.config import Config
from v2.src.core.utils.allure_utils import AllureReporter

CATEGORIES_FILE = Path(__file__).parent.parent / 'resources' / 'categories.json'


@pytest.fixture(scope='session', autouse=True)
def allure_setup(request):
    """Setup Allure reporting."""

    def finalizer():
        allure_dir = request.config.getoption('--alluredir', None)
        reporter = AllureReporter(allure_dir)
        reporter.setup(
            env=Config.ENV, base_url=Config.BASE_URL, categories_file=CATEGORIES_FILE
        )

    request.addfinalizer(finalizer)
