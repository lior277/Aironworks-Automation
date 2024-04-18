import allure
from enum import Enum
from src.models.user_model import UserModel
from playwright.sync_api import APIRequestContext


class LoginApi(Enum):
    API_VERSION = "/api"

    LOGIN = "/auth/login"

    INFO = "/auth/info"

    PICK_ROLE = "/auth/pick_role"


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

    @classmethod
    @allure.step("LoginService: get self info")
    def info(cls, request_context: APIRequestContext):
        return request_context.get(
            LoginApi.API_VERSION.value + LoginApi.INFO.value,
        )

    @classmethod
    @allure.step("LoginService: pick role")
    def pick_role(cls, request_context: APIRequestContext, role_id: str):
        return request_context.post(
            LoginApi.API_VERSION.value + LoginApi.PICK_ROLE.value,
            data={"role_id": role_id},
        )
