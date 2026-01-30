# v2/src/core/utils/allure_utils.py
"""Allure reporting utilities."""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class AllureEnvironment:
    """Allure environment configuration."""

    env: str
    base_url: str
    browser_name: str = 'unknown'
    browser_version: str = 'unknown'

    def write(self, allure_dir: str) -> None:
        """Write environment.properties file."""
        env_file = Path(allure_dir) / 'environment.properties'
        env_file.write_text(
            f'ENV={self.env}\n'
            f'BASE_URL={self.base_url}\n'
            f'BROWSER_NAME={self.browser_name}\n'
            f'BROWSER_VERSION={self.browser_version}\n'
        )


class GitLabExecutor:
    """GitLab CI executor info for Allure."""

    @classmethod
    def from_env(cls) -> dict[str, str] | None:
        """Create from GitLab CI environment variables."""
        if not os.environ.get('CI_PIPELINE_IID'):
            return None

        return {
            'type': 'gitlab',
            'name': os.environ.get('CI_PROJECT_PATH', ''),
            'url': os.environ.get('CI_PROJECT_URL', ''),
            'buildOrder': os.environ.get('CI_PIPELINE_IID', ''),
            'buildName': os.environ.get('CI_JOB_NAME', ''),
            'buildUrl': os.environ.get('CI_JOB_URL', ''),
            'reportName': 'Allure Report',
        }

    @classmethod
    def write(cls, allure_dir: str) -> None:
        """Write executor.json if in GitLab CI."""
        if executor := cls.from_env():
            executor_file = Path(allure_dir) / 'executor.json'
            executor_file.write_text(json.dumps(executor, indent=2))


class AllureReporter:
    """Allure report configuration."""

    def __init__(self, allure_dir: str | None):
        self.allure_dir = allure_dir

    def setup(
        self,
        env: str,
        base_url: str,
        categories: list[dict[str, Any]] | None = None,  # ✅ FIXED
    ) -> None:
        """Setup Allure environment, executor, and categories."""
        if not self.allure_dir:
            return

        # Environment
        AllureEnvironment(
            env=env,
            base_url=base_url,
            browser_name=os.getenv('BROWSER_NAME', 'unknown'),
            browser_version=os.getenv('BROWSER_VERSION', 'unknown'),
        ).write(self.allure_dir)

        # Executor
        GitLabExecutor.write(self.allure_dir)

        # Categories
        if categories:
            categories_file = Path(self.allure_dir) / 'categories.json'
            categories_file.write_text(json.dumps(categories, indent=2))
