import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _as_bool(v: str | None, default: bool = False) -> bool:
    if v is None:
        return default
    return v.strip().lower() in ('1', 'true', 'yes', 'y', 'on')


def _get_env_int(key: str, default: int = 0, json_key: str | None = None) -> int:
    """Get integer from env or JSON file"""
    env_val = os.getenv(key)
    if env_val:
        return int(env_val.strip())
    if json_key and json_key in _ENV_DATA:
        return int(_ENV_DATA[json_key])
    return default


def _get_env_str(key: str, default: str = '', json_key: str | None = None) -> str:
    """Get string from env or JSON file"""
    env_val = os.getenv(key)
    if env_val:
        return env_val.strip()
    if json_key and json_key in _ENV_DATA:
        return str(_ENV_DATA[json_key]).strip()
    return default


# Load environment data once
_ENV = os.getenv('ENV', 'local')
_ENV_FILE = _repo_root() / 'v2' / 'envs' / f'{_ENV}.json'
_ENV_DATA = json.loads(_ENV_FILE.read_text()) if _ENV_FILE.exists() else {}


class Config:
    """Application configuration"""

    ENV: str = _ENV

    # URLs
    APP_BASE_URL: str = _get_env_str('APP_BASE_URL', json_key='base_url').rstrip('/')
    ADMIN_BASE_URL: str = _get_env_str(
        'ADMIN_BASE_URL', json_key='admin_base_url'
    ).rstrip('/')

    # Browser
    HEADLESS: bool = _as_bool(os.getenv('HEADLESS'), default=True)
    BROWSER: str = os.getenv('BROWSER', 'chromium')
    DEFAULT_TIMEOUT_SEC: int = _get_env_int('DEFAULT_TIMEOUT_SEC', default=30)
    EXPECT_TIMEOUT_MS: int = _get_env_int('EXPECT_TIMEOUT_MS', default=20000)

    # Customer admin
    CUSTOMER_EMAIL: str = _get_env_str('CUSTOMER_EMAIL')
    CUSTOMER_PASSWORD: str = _get_env_str('CUSTOMER_PASSWORD')
    CUSTOMER_ROLE_ID: str = _get_env_str('CUSTOMER_ROLE_ID')

    # API
    API_RETRIES: int = _get_env_int('API_RETRIES', default=2)
    API_RETRY_DELAY_SEC: float = float(os.getenv('API_RETRY_DELAY_SEC', '1.0'))
    API_RETRY_ON_STATUS: tuple[int, ...] = (500, 502, 503, 504)

    # Mailtrap
    MAILTRAP_BASE_URL: str = _get_env_str(
        'MAILTRAP_BASE_URL', default='https://mailtrap.io'
    ).rstrip('/')
    MAILTRAP_API_TOKEN: str = _get_env_str('MAILTRAP_API_TOKEN')
    MAILTRAP_ACCOUNT_ID: int = _get_env_int(
        'MAILTRAP_ACCOUNT_ID', json_key='mailtrap_account_id'
    )
    MAILTRAP_API_PREFIX: str = '/' + _get_env_str(
        'MAILTRAP_API_PREFIX', default='/api', json_key='mailtrap_api_prefix'
    ).strip().lstrip('/')
    MAILTRAP_TIMEOUT_SEC: int = _get_env_int('MAILTRAP_TIMEOUT_SEC', default=60)
    MAILTRAP_POLL_INTERVAL_SEC: float = float(
        os.getenv('MAILTRAP_POLL_INTERVAL_SEC', '1.0')
    )
    MAILTRAP_MAX_PAGES: int = _get_env_int('MAILTRAP_MAX_PAGES', default=5)
    MAILTRAP_ASSESSMENT_INBOX_ID: int = _get_env_int(
        'MAILTRAP_ASSESSMENT_INBOX_ID', json_key='mailtrap_assessment_inbox_id'
    )
    MAILTRAP_ASSESSMENT_INBOX_MAIL: str = _get_env_str(
        'MAILTRAP_ASSESSMENT_INBOX_MAIL', json_key='mailtrap_assessment_inbox_mail'
    )
