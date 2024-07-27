from dataclasses import asdict

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.models.auth.signup_model import EmailSignupModel
from src.models.auth.user_model import UserModel
from .base_service import BaseService
from .psapi import PSApi


class LoginService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('LoginService: submit login')
    def login(self, user: UserModel) -> APIResponse:
        return self._post(
            PSApi.LOGIN.get_endpoint(),
            data={
                'admin': user.is_admin,
                'email': user.email,
                'password': user.password,
                'remember': True,
            },
        )

    @allure.step('LoginService: get self info')
    def info(self) -> APIResponse:
        return self._get(PSApi.INFO.get_endpoint())

    @allure.step('LoginService: pick role')
    def pick_role(self, role_id: str) -> APIResponse:
        return self._post(PSApi.PICK_ROLE.get_endpoint(), data={'role_id': role_id})

    @allure.step('LoginService: register a customer')
    def register(self, signup: EmailSignupModel) -> APIResponse:
        return self._post(PSApi.REGISTER.get_endpoint(), data=asdict(signup))
