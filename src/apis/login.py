from dataclasses import asdict
from playwright.sync_api import APIRequestContext
from src.models.user_model import UserModel
from src.models.signup_model import EmailSignupModel
from .psapi import PSApi
import allure


class LoginService:
    @classmethod
    @allure.step("LoginService: submit login")
    def login(cls, request_context: APIRequestContext, user: UserModel):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.LOGIN.value,
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
            PSApi.API_VERSION.value + PSApi.INFO.value,
        )

    @classmethod
    @allure.step("LoginService: pick role")
    def pick_role(cls, request_context: APIRequestContext, role_id: str):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.PICK_ROLE.value,
            data={"role_id": role_id},
        )

    @classmethod
    @allure.step("LoginService: register a customer")
    def register(cls, request_context: APIRequestContext, signup: EmailSignupModel):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.REGISTER.value, data=asdict(signup)
        )
