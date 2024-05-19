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
    ADMIN_BASE_URL = _env_config["admin_base_url"]
    ADDIN_BASE_URL = _env_config["addin_base_url"]
    EXAMPLE_SCENARIO = _env_config["example_scenario"]
    EXAMPLE_EDUCATION_CONTENT = _env_config["example_education_content"]

    LOGIN_SA_ACCOUNT = os.getenv("LOGIN_SA_ACCOUNT")
    MAILTRAP_API_TOKEN = os.getenv("MAILTRAP_API_TOKEN")
    CUSTOMER_ADMIN_USERNAME = os.getenv("CUSTOMER_ADMIN_USERNAME")
    CUSTOMER_ADMIN_PASSWORD = os.getenv("CUSTOMER_ADMIN_PASSWORD")
    AW_ADMIN_USERNAME = os.getenv("AW_ADMIN_USERNAME")
    AW_ADMIN_PASSWORD = os.getenv("AW_ADMIN_PASSWORD")
    RESELLER_ADMIN_USERNAME = os.getenv("RESELLER_ADMIN_USERNAME")
    RESELLER_ADMIN_PASSWORD = os.getenv("RESELLER_ADMIN_PASSWORD")

    MAILTRAP_ASSESSMENT_INBOX_ID = _env_config["mailtrap_assessment_inbox_id"]
    MAILTRAP_ASSESSMENT_INBOX_MAIL = _env_config["mailtrap_assessment_inbox_mail"]
    MAILTRAP_ACCOUNT_ID = _env_config["mailtrap_account_id"]

    EMPLOYEE_INBOX = "fae1336c2d-da5a02+%s@inbox.mailtrap.io"
    EMPLOYEE_INBOX_ID = 2813733
