import os


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://your-aironworks-url")
    API_BASE_URL = os.getenv("API_BASE_URL", BASE_URL)

    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "20"))

    USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@company.com")
    USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Password123!")

    BASE_URL = os.getenv("BASE_URL")
    API_KEY = os.getenv("API_KEY")
