from dataclasses import asdict

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.models.auth.signup_model import EmailSignupModel
from src.models.auth.user_model import UserModel
from .psapi import PSApi


class LoginService:
    @classmethod
    @allure.step("LoginService: submit login")
    def login(cls, request_context: APIRequestContext, user: UserModel) -> APIResponse:
        return request_context.post(
            PSApi.LOGIN.get_endpoint(),
            data={
                "admin": user.is_admin,
                "email": user.email,
                "password": user.password,
                "remember": True,
            },
        )

    @classmethod
    @allure.step("LoginService: get self info")
    def info(cls, request_context: APIRequestContext) -> APIResponse:
        return request_context.get(PSApi.INFO.get_endpoint())

    @classmethod
    @allure.step("LoginService: pick role")
    def pick_role(cls, request_context: APIRequestContext, role_id: str) -> APIResponse:
        return request_context.post(
            PSApi.PICK_ROLE.get_endpoint(),
            data={"role_id": role_id},
        )

    @classmethod
    @allure.step("LoginService: register a customer")
    def register(
        cls, request_context: APIRequestContext, signup: EmailSignupModel
    ) -> APIResponse:
        return request_context.post(PSApi.REGISTER.get_endpoint(), data=asdict(signup))
