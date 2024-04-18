import allure
from enum import Enum
from src.models.user_model import UserModel
from playwright.sync_api import APIRequestContext


class LoginApi(Enum):
    API_VERSION = "/api"

    LOGIN = "/auth/login"


class LoginService:
    @classmethod
    @allure.step("LoginService: submit login")
    def login(cls, request_context: APIRequestContext, user: UserModel):
        return request_context.post(
            LoginApi.API_VERSION.value + LoginApi.LOGIN.value,
            data={
                "admin": user.is_admin,
                "email": user.email,
                "password": user.password,
                "remember": True,
            },
        )
