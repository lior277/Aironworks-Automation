import os

from dotenv import load_dotenv, find_dotenv

from src.configs.config_utils import get_env_config


class AppFolders:
    # paths to directories
    CUR_DIR_PATH = os.getcwd()
    SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    TESTS_PATH = os.path.abspath(os.path.join(SRC_PATH, os.pardir, "tests"))
    FILES_PATH = os.path.join(TESTS_PATH, 'resources/files/')
    TMP_FILES_PATH = os.path.join(TESTS_PATH, 'resources/tmp/')


class AppConfigs:
    # load to environment variables our test env name
    load_dotenv(find_dotenv())

    # load test environment configs1
    ENV = os.getenv("ENV")

    _env_config = get_env_config(ENV)

    BASE_URL = _env_config["base_url"]
    # AUTH_URL = _env_config["auth_url"]
    # STATIC_URL = _env_config["static_url"]

    # ENV CONFIGS
    # DRIVER_ID = _env_config["go_mobile_user"]

    # WebDriver wait
    # UI_MAX_RESPONSE_TIME = 15.0

    # WebDriver
    WEB_DRIVER = os.getenv("WEB_DRIVER")
    HEADLESS = os.getenv("HEADLESS") == "True"
