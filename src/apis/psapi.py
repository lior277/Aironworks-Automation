from enum import Enum


class PSApi(Enum):
    API_VERSION = "/api"

    UPLOAD_EMPLOYEE_INFO = "/company/upload_employee_info"
    EMPLOYEE_LIST = "/company/employee_list"
    EMPLOYEE_LIST_IDS = "/company/employee_list_ids"
    EMPLOYEE_UPDATE = "/company/employee_update"
    EMPLOYEE_DELETE = "/company/employee_delete"
    COMPANY_LOCALIZED_CONFIG = "/company/localized-configs"

    LOGIN = "/auth/login"
    INFO = "/auth/info"
    PICK_ROLE = "/auth/pick_role"
    REGISTER = "/auth/register"
    LOGOUT = "/auth/logout"
    VERIFY_URL_CLICK = "/public/verify_url_click"

    CAMPAIGN = "/admin/campaign"
    GET_ATTACK_EXECUTION = "/admin/get_attack_execution"
    COMPANY_COUNT = "/admin/company_count"

    EDUCATION_CAMPAIGN = "/education/campaign"
    EDUCATION_LIBRARY_DATA = "/education/library_data"
    EDUCATION_CONTENT = "/education/content"
    # For Performance testing only
    ADMIN_EDUCATION_ASSIGNMENTS = "/admin/education_assignments/{campaign_id}"

    def get_endpoint(self):
        return self.API_VERSION.value + self.value
