import allure
from playwright.sync_api import APIRequestContext, APIResponse

from .base_service import BaseService
from .psapi import PSApi


class EmailFilterService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('EmailFilterService: block email')
    def block_email(self, email: str) -> APIResponse:
        data = {'blocked_email': {'type': 'BLOCKED_EMAIL_TYPE_EMAIL', 'link': email}}
        return self._post(PSApi.BLOCK_EMAIL.get_endpoint().format(), data=data)

    @allure.step('EmailFilterService: block domain')
    def block_domain(self, domain: str) -> APIResponse:
        data = {'blocked_email': {'type': 'BLOCKED_EMAIL_TYPE_DOMAIN', 'link': domain}}
        return self._post(PSApi.BLOCK_EMAIL.get_endpoint().format(), data=data)

    @allure.step('EmailFilterService: unblock email/domain')
    def unblock_email_domain(self, email_id: str) -> APIResponse:
        return self._delete(PSApi.UNBLOCK_EMAIL.get_endpoint().format(id=email_id))

    @allure.step('EmailFilterService: safe email')
    def safe_email(self, email: str) -> APIResponse:
        data = {'safe_email': {'type': 'BLOCKED_EMAIL_TYPE_EMAIL', 'link': email}}
        return self._post(PSApi.SAFE_EMAIL.get_endpoint().format(), data=data)

    @allure.step('EmailFilterService: safe domain')
    def safe_domain(self, domain: str) -> APIResponse:
        data = {'safe_email': {'type': 'BLOCKED_EMAIL_TYPE_DOMAIN', 'link': domain}}
        return self._post(PSApi.SAFE_EMAIL.get_endpoint().format(), data=data)

    @allure.step('EmailFilterService: unsafe email/domain')
    def unsafe_email_domain(self, email_id: str) -> APIResponse:
        return self._delete(PSApi.UNSAFE_EMAIL.get_endpoint().format(id=email_id))

    @allure.step('EmailFilterService: list safe emails/domains')
    def list_safe_emails_domains(self) -> APIResponse:
        params = {'page_size': 15, 'offset': 0}
        return self._get(PSApi.SAFE_LIST.get_endpoint().format(), params=params)

    @allure.step('EmailFilterService: list blocked emails/domains')
    def list_blocked_emails_domains(self) -> APIResponse:
        params = {'page_size': 15, 'offset': 0}
        return self._get(PSApi.BLOCKED_LIST.get_endpoint().format(), params=params)

    @allure.step('EmailFilterService: list safe emails/domains')
    def list_unsafe_emails_domains(self) -> APIResponse:
        return self._get(PSApi.SAFE_LIST.get_endpoint().format())

    @allure.step('EmailFilterService: label as high-risk only')
    def label_as_high_risk(self, email: str) -> APIResponse:
        data = {'high_risk_mail_behavior': 'HIGH_RISK_MAIL_BEHAVIOR_TYPE_LABEL'}
        return self._post(PSApi.HIGH_RISK_HANDLING.get_endpoint().format(), data=data)

    @allure.step('EmailFilterService: block high-risk')
    def block_high_risk(self, email: str) -> APIResponse:
        data = {'high_risk_mail_behavior': 'HIGH_RISK_MAIL_BEHAVIOUR_BLOCK'}
        return self._post(PSApi.HIGH_RISK_HANDLING.get_endpoint().format(), data=data)
