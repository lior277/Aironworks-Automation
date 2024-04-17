import os

from dotenv import load_dotenv, find_dotenv

from src.configs.config_utils import get_env_config


class AppFolders:
    # paths to directories
    CUR_DIR_PATH = os.getcwd()
    SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    TESTS_PATH = os.path.abspath(os.path.join(SRC_PATH, os.pardir, "tests"))
    RESOURCES_PATH = os.path.join(TESTS_PATH, "resources/")
    FILES_PATH = os.path.join(TESTS_PATH, "resources/files/")
    TMP_FILES_PATH = os.path.join(TESTS_PATH, "resources/tmp/")


class AppConfigs:
    # load to environment variables our test env name
    load_dotenv(find_dotenv())

    # load test environment configs1
    ENV = os.getenv("ENV")

    _env_config = get_env_config(ENV)

    BASE_URL = _env_config["base_url"]
    ADDIN_BASE_URL = _env_config["addin_base_url"]


    LOGIN_SA_ACCOUNT = os.getenv("LOGIN_SA_ACCOUNT")
    MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")

    MAILTRAP_ASSESSMENT_INBOX_ID = _env_config["mailtrap_assessment_inbox_id"]
    MAILTRAP_ASSESSMENT_INBOX_MAIL = _env_config["mailtrap_assessment_inbox_mail"]
    MAILTRAP_ACCOUNT_ID = _env_config["mailtrap_account_id"]
