from playwright.sync_api import APIRequestContext

from src.apis.admin import AdminService


class ServiceFactory:

    @staticmethod
    def admin(request_context: APIRequestContext):
        return AdminService(request_context)


api = ServiceFactory()
