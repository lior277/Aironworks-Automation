"""Configuration from environment variables."""

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Config:
    ENV = os.getenv('ENV', 'staging')

    BASE_URL = os.getenv('BASE_URL', 'https://staging.app.aironworks.com')

    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '30'))

    # Auth credentials
    USER_EMAIL = os.getenv('USER_EMAIL', '')
    USER_PASSWORD = os.getenv('USER_PASSWORD', '')

    # Optional: specific role to pick (empty = first role)
    USER_ROLE_ID = os.getenv('USER_ROLE_ID', '')
