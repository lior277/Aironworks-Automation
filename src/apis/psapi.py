from enum import Enum


class PSApi(Enum):
    API_VERSION = "/api"
    UPLOAD_URL = "/upload/url"

    UPLOAD_EMPLOYEE_INFO = "/company/upload_employee_info"
    UPLOAD_EMPLOYEE_INFO_STATUS = "/company/upload_employee_info/{op_id}"
    EMPLOYEE_LIST = "/company/employee_list"
    EMPLOYEE_LIST_IDS = "/company/employee_list_ids"
    EMPLOYEE_UPDATE = "/company/employee_update"
    EMPLOYEE_DELETE = "/company/employee_delete"
    COMPANY_LOCALIZED_CONFIG = "/company/localized-configs"
    COMPANY_LOCALIZED_CONFIG_LANGUAGE = "/company/localized-configs/{language}"

    LOGIN = "/auth/login"
    INFO = "/auth/info"
    PICK_ROLE = "/auth/pick_role"
    REGISTER = "/auth/register"
    LOGOUT = "/auth/logout"
    VERIFY_URL_CLICK = "/public/verify_url_click"

    CAMPAIGN = "/admin/campaign"
    LIST_ATTACK_INFOS = "/admin/list_attack_infos"
    GET_ATTACK_INFO = "admin/get_attack_info"
    GET_ATTACK_EXECUTION = "/admin/get_attack_execution"
    COMPANY_COUNT = "/admin/company_count"
    DEACTIVATE_COMPANY = "/admin/company/{company_id}/deactivate"
    COMPANIES_LIST = "/admin/company"

    EDUCATION_CAMPAIGN = "/education/campaign"
    EDUCATION_CAMPAIGN_DETAILS = "/education/campaign/{campaign_id}"
    EDUCATION_LIBRARY_DATA = "/education/library_data"
    EDUCATION_CONTENT = "/education/content"
    EDUCATION_CONTENT_DETAILS = "/education/content/{content_id}"
    EDUCATION_CAMPAIGN_LIST = "/education/campaign_list"
    # customer
    CUSTOMER_ATTACK_PAGE_PREVIEW = "/customer/attack_page_preview"

    # Surveys
    LIST_SURVEYS = "/survey/list_surveys"
    ADD_SURVEY = "/survey/add_survey"
    DELETE_SURVEY = "/survey/delete_survey"
    SET_DEFAULT_SURVEY = "/survey/set_default_survey"
    GET_SURVEY = "/survey/get_survey"
    GET_SPECIFIC_SURVEY_ANSWER_STATS = "/survey/get_specific_survey_answer_stats"
    # For Performance testing only
    ADMIN_EDUCATION_ASSIGNMENTS = "/admin/education_assignments/{campaign_id}"
    ADMIN_CAMPAIGN_ATTACK_URLS = "/admin/campaign/{campaign_id}/attack_urls"

    def get_endpoint(self):
        return self.API_VERSION.value + self.value
