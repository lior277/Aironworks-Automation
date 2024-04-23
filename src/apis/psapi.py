from enum import Enum


class PSApi(Enum):
    API_VERSION = "/api"

    UPLOAD_EMPLOYEE_INFO = "/company/upload_employee_info"
    EMPLOYEE_LIST = "/company/employee_list"

    LOGIN = "/auth/login"
    INFO = "/auth/info"
    PICK_ROLE = "/auth/pick_role"
    VERIFY_URL_CLICK = "/public/verify_url_click"

    CAMPAIGN = "/admin/campaign"
    GET_ATTACK_EXECUTION = "/admin/get_attack_execution"
