import os

from dotenv import load_dotenv, find_dotenv

from src.configs.config_utils import get_env_config


class AppFolders:
    # paths to directories
    CUR_DIR_PATH = os.getcwd()
    SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    TESTS_PATH = os.path.abspath(os.path.join(SRC_PATH, os.pardir, 'tests'))
    RESOURCES_PATH = os.path.join(TESTS_PATH, 'resources/')
    FILES_PATH = os.path.join(TESTS_PATH, 'resources/files/')
    TMP_FILES_PATH = os.path.join(TESTS_PATH, 'resources/tmp/')


class AppConfigs:
    # load to environment variables our test env name
    load_dotenv(find_dotenv())

    # load test environment configs1
    ENV = os.getenv('ENV')

    _env_config = get_env_config(ENV)

    BASE_URL = _env_config['base_url']
    ADMIN_BASE_URL = _env_config['admin_base_url']
    ADDIN_BASE_URL = _env_config['addin_base_url']
    ADDIN_NAME = _env_config['addin_name']
    EXAMPLE_SCENARIO = _env_config['example_scenario']
    EXAMPLE_SCENARIO_NAME = _env_config['example_scenario_name']
    EXAMPLE_EDUCATION_CONTENT = _env_config['example_education_content']
    LINKS_DOMAIN = _env_config['links_domain']
    SENDER_DOMAIN = _env_config['sender_domain']
    SAMPLE_CAMPAIGN = _env_config['sample_campaign']
    SAMPLE_CAMPAIGN_NAME = _env_config['sample_campaign_name']

    LOGIN_SA_ACCOUNT = os.getenv('LOGIN_SA_ACCOUNT')
    MAILTRAP_API_TOKEN = os.getenv('MAILTRAP_API_TOKEN')
    CUSTOMER_ADMIN_USERNAME = os.getenv('CUSTOMER_ADMIN_USERNAME')
    CUSTOMER_ADMIN_PASSWORD = os.getenv('CUSTOMER_ADMIN_PASSWORD')
    AW_ADMIN_USERNAME = os.getenv('AW_ADMIN_USERNAME')
    AW_ADMIN_PASSWORD = os.getenv('AW_ADMIN_PASSWORD')
    RESELLER_ADMIN_USERNAME = os.getenv('RESELLER_ADMIN_USERNAME')
    RESELLER_ADMIN_PASSWORD = os.getenv('RESELLER_ADMIN_PASSWORD')

    MAILTRAP_ASSESSMENT_INBOX_ID = _env_config['mailtrap_assessment_inbox_id']
    MAILTRAP_ASSESSMENT_INBOX_MAIL = _env_config['mailtrap_assessment_inbox_mail']
    MAILTRAP_ACCOUNT_ID = _env_config['mailtrap_account_id']

    EMPLOYEE_INBOX = 'fae1336c2d-da5a02+%s@inbox.mailtrap.io'
    EMPLOYEE_INBOX_ID = 2813733
    # PERF INBOXES
    PERF_EMPLOYEE_INBOX = '9f9583b92f-4a60a4+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_1 = 'a3965d431d-41958b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_2 = 'ebfaaba517-21a015+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_3 = 'c1abf52c17-afed88+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_4 = '63d4d90aa7-cd749b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_5 = '1eaee4f7d4-7f16ba+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_6 = '657974782f-8cfbd9+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_7 = '97e3d6f841-de2962+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_8 = '8b16b72b19-1770a5+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_9 = 'd03a2acce8-874618+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_10 = '242ec4355a-b8f694+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_11 = '4b6465112f-10b69e+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_12 = 'b680f3fb40-edb379+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_13 = 'd520a7e55e-c5825c+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_14 = '9c6107c2d5-3271d7+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_15 = '24e6365de3-932b3b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_16 = '86f914bb25-72a599+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_17 = 'aa04f9cbab-725254+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_18 = '347168cb85-623d3c+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_19 = 'c95fb1fd87-d6f3aa+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_20 = '4675d48bcd-8425d5+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_21 = 'd61cd0e3aa-28c1d9+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_22 = '61de5ef72f-cae08b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_23 = '840c77c315-d2c585+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_24 = 'b433844a56-4aaa3b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_25 = 'fe9f6e6799-e896ed+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_26 = 'b508caa92d-886739+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_27 = '2584e8e8b9-cc3216+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_28 = '234c7ccd34-259238+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_29 = '069496178f-413e1b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_30 = '327c54fab5-121fad+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_31 = '5a2c45f230-bfdf08+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_32 = '0d4d9a0b7a-3d6e12+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_33 = 'deabd156c4-1ea1c7+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_34 = '6826be74b8-5bb746+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_35 = '0ed44cd855-6ea2a3+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_36 = '809135c50c-a0f9db+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_37 = '6e6a2e7ca8-534e8d+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_38 = '05c064b246-7eebdc+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_39 = '2139b2bf57-df2273+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_40 = 'a377638cc9-228584+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_41 = '1984915174-ffa503+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_42 = '92e2550a52-51943b+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_43 = '860a301df0-ff535c+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_44 = '153ca5d6c3-71cdf7+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_45 = '5f6770a9c6-501e52+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_46 = '8ef783a3bf-24b568+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_47 = '5ae6d75c21-b23af8+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_48 = '5e23110809-98cec0+%s@inbox.mailtrap.io'
    PERF_EMPLOYEE_INBOX_49 = '526d41bb1b-e08be3+%s@inbox.mailtrap.io'

    PERF_EMPLOYEE_INBOX_ID = 2935468
    PERF_EMPLOYEE_INBOX_ID_1 = 2935611
    PERF_EMPLOYEE_INBOX_ID_2 = 2935836
    PERF_EMPLOYEE_INBOX_ID_3 = 2935837
    PERF_EMPLOYEE_INBOX_ID_4 = 2935838
    PERF_EMPLOYEE_INBOX_ID_5 = 2935839
    PERF_EMPLOYEE_INBOX_ID_6 = 2935840
    PERF_EMPLOYEE_INBOX_ID_7 = 2935841
    PERF_EMPLOYEE_INBOX_ID_8 = 2935842
    PERF_EMPLOYEE_INBOX_ID_9 = 2935843
    PERF_EMPLOYEE_INBOX_ID_10 = 2936288
    PERF_EMPLOYEE_INBOX_ID_11 = 2936289
    PERF_EMPLOYEE_INBOX_ID_12 = 2936290
    PERF_EMPLOYEE_INBOX_ID_13 = 2936291
    PERF_EMPLOYEE_INBOX_ID_14 = 2936292
    PERF_EMPLOYEE_INBOX_ID_15 = 2936293
    PERF_EMPLOYEE_INBOX_ID_16 = 2936294
    PERF_EMPLOYEE_INBOX_ID_17 = 2936295
    PERF_EMPLOYEE_INBOX_ID_18 = 2936296
    PERF_EMPLOYEE_INBOX_ID_19 = 2936298
    PERF_EMPLOYEE_INBOX_ID_20 = 2936299
    PERF_EMPLOYEE_INBOX_ID_21 = 2936300
    PERF_EMPLOYEE_INBOX_ID_22 = 2936301
    PERF_EMPLOYEE_INBOX_ID_23 = 2936302
    PERF_EMPLOYEE_INBOX_ID_24 = 2936303
    PERF_EMPLOYEE_INBOX_ID_25 = 2936304
    PERF_EMPLOYEE_INBOX_ID_26 = 2936305
    PERF_EMPLOYEE_INBOX_ID_27 = 2936306
    PERF_EMPLOYEE_INBOX_ID_28 = 2936307
    PERF_EMPLOYEE_INBOX_ID_29 = 2936308
    PERF_EMPLOYEE_INBOX_ID_30 = 2936310
    PERF_EMPLOYEE_INBOX_ID_31 = 2936311
    PERF_EMPLOYEE_INBOX_ID_32 = 2936312
    PERF_EMPLOYEE_INBOX_ID_33 = 2936313
    PERF_EMPLOYEE_INBOX_ID_34 = 2936314
    PERF_EMPLOYEE_INBOX_ID_35 = 2936315
    PERF_EMPLOYEE_INBOX_ID_36 = 2936316
    PERF_EMPLOYEE_INBOX_ID_37 = 2936317
    PERF_EMPLOYEE_INBOX_ID_38 = 2936318
    PERF_EMPLOYEE_INBOX_ID_39 = 2936319
    PERF_EMPLOYEE_INBOX_ID_40 = 2936320
    PERF_EMPLOYEE_INBOX_ID_41 = 2936321
    PERF_EMPLOYEE_INBOX_ID_42 = 2936322
    PERF_EMPLOYEE_INBOX_ID_43 = 2936323
    PERF_EMPLOYEE_INBOX_ID_44 = 2936325
    PERF_EMPLOYEE_INBOX_ID_45 = 2936324
    PERF_EMPLOYEE_INBOX_ID_46 = 2936326
    PERF_EMPLOYEE_INBOX_ID_47 = 2936328
    PERF_EMPLOYEE_INBOX_ID_48 = 2936329
    PERF_EMPLOYEE_INBOX_ID_49 = 2936330

    QA_COMPANY_NAME = 'QA Accounts'

    MSLIVE_USER = os.getenv('MSLIVE_USER')
    MSLIVE_PWD = os.getenv('MSLIVE_PWD')
    MSLIVE_TOTP = os.getenv('MSLIVE_TOTP')
