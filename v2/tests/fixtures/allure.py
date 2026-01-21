"""Allure reporting fixtures."""

import json
import os

import allure
import pytest

from v2.src.core.config import Config


@pytest.fixture(scope='session', autouse=True)
@allure.title('Populate allure environment')
def allure_environment(request):
    """Write environment info to Allure report."""

    def finalizer():
        allure_dir = request.config.getoption('--alluredir', None)
        if not allure_dir:
            return

        with open(os.path.join(allure_dir, 'environment.properties'), 'w') as f:
            f.write(f'ENV={Config.ENV}\n')
            f.write(f'BASE_URL={Config.BASE_URL}\n')
            f.write(f'BROWSER_NAME={os.getenv("BROWSER_NAME", "unknown")}\n')
            f.write(f'BROWSER_VERSION={os.getenv("BROWSER_VERSION", "unknown")}\n')

        if os.environ.get('CI_PIPELINE_IID'):
            executor = {
                'type': 'gitlab',
                'name': os.environ['CI_PROJECT_PATH'],
                'url': os.environ['CI_PROJECT_URL'],
                'buildOrder': os.environ['CI_PIPELINE_IID'],
                'buildName': os.environ['CI_JOB_NAME'],
                'buildUrl': os.environ['CI_JOB_URL'],
                'reportName': 'Allure Report',
            }
            with open(os.path.join(allure_dir, 'executor.json'), 'w') as f:
                json.dump(executor, f)

    request.addfinalizer(finalizer)
