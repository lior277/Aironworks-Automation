from playwright.sync_api import APIRequestContext

from src.apis.admin import AdminService
from src.apis.company import CompanyService
from src.apis.education import EducationService
from src.apis.login import LoginService
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


api = ServiceFactory()
