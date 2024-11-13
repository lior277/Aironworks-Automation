from playwright.sync_api import APIRequestContext

from src.apis.admin import AdminService
from src.apis.assessment import AssessmentService
from src.apis.company import CompanyService
from src.apis.customer import CustomerService
from src.apis.education import EducationService
from src.apis.email_filter import EmailFilterService
from src.apis.group_service import GroupService
from src.apis.login import LoginService
from src.apis.phish_detect_ai_service import PhishDetectUI
from src.apis.public import PublicService
from src.apis.scenario import ScenarioService
from src.apis.survey_service import SurveyService
from src.apis.upload import UploadService


class ServiceFactory:
    @staticmethod
    def admin(request_context: APIRequestContext) -> AdminService:
        return AdminService(request_context)

    @staticmethod
    def company(request_context: APIRequestContext) -> CompanyService:
        return CompanyService(request_context)

    @staticmethod
    def upload(request_context: APIRequestContext) -> UploadService:
        return UploadService(request_context)

    @staticmethod
    def education(request_context: APIRequestContext) -> EducationService:
        return EducationService(request_context)

    @staticmethod
    def login(request_context: APIRequestContext) -> LoginService:
        return LoginService(request_context)

    @staticmethod
    def assessment(request_context: APIRequestContext) -> AssessmentService:
        return AssessmentService(request_context)

    @staticmethod
    def public(request_context: APIRequestContext) -> PublicService:
        return PublicService(request_context)

    @staticmethod
    def customer(request_context: APIRequestContext) -> CustomerService:
        return CustomerService(request_context)

    @staticmethod
    def scenario(request_context: APIRequestContext) -> ScenarioService:
        return ScenarioService(request_context)

    @staticmethod
    def survey(request_context: APIRequestContext) -> SurveyService:
        return SurveyService(request_context)

    @staticmethod
    def group(request_context: APIRequestContext) -> GroupService:
        return GroupService(request_context)

    @staticmethod
    def phish_detect_ui_settings(request_context: APIRequestContext) -> PhishDetectUI:
        return PhishDetectUI(request_context)

    @staticmethod
    def email_filter(request_context: APIRequestContext) -> EmailFilterService:
        return EmailFilterService(request_context)


api = ServiceFactory()
