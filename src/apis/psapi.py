from enum import Enum
from playwright.sync_api import APIRequestContext, expect
from csv import DictWriter
from typing import List
import io
from base64 import b64encode
import allure
from src.models.user_model import UserModel
from src.models.campaign_model import CampaignModel


class PSApi(Enum):
    API_VERSION = "/api"

    UPLOAD_EMPLOYEE_INFO = "/company/upload_employee_info"
    EMPLOYEE_LIST = "/company/employee_list"

    LOGIN = "/auth/login"
    INFO = "/auth/info"
    PICK_ROLE = "/auth/pick_role"
    VERIFY_URL_CLICK = "/public/verify_url_click"

    CAMPAIGN = "/admin/campaign"
    GET_ATTACK_EXECUTION = "/admin/get_attack_execution"


class PSService:
    @classmethod
    def create_employee(
        cls,
        request_context: APIRequestContext,
        employee_mail: str,
        employee_first_name: str,
        employee_last_name: str,
    ):
        buffer = io.StringIO()
        writer = DictWriter(buffer, fieldnames=["first_name", "last_name", "email"])
        writer.writerow(
            {"first_name": "First Name", "last_name": "Last Name", "email": "Email"}
        )
        writer.writerow(
            {
                "first_name": employee_first_name,
                "last_name": employee_last_name,
                "email": employee_mail,
            }
        )
        buffer.flush()
        buffer.seek(0, 0)
        data = b64encode(buffer.read().encode("utf-8")).decode("utf-8")
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.UPLOAD_EMPLOYEE_INFO.value,
            data={
                "file_path": "random_path.csv",
                "file_text": data,
                "overwrite": False,
            },
        )

    @classmethod
    def employee_by_mail(cls, request_context: APIRequestContext, email: str):
        result = request_context.post(
            PSApi.API_VERSION.value + PSApi.EMPLOYEE_LIST.value,
            data={
                "employee_role": True,
                "filters": {
                    "items": [
                        {
                            "columnField": "email",
                            "operatorValue": "contains",
                            "id": 0,
                            "value": email,
                        }
                    ],
                    "linkOperator": "and",
                    "quickFilterValues": [],
                    "quickFilterLogicOperator": "and",
                },
                "offset": 0,
                "limit": 1,
                "sorting": [],
            },
        )
        expect(result).to_be_ok()
        data = result.json()
        assert "items" in data
        assert len(data["items"]) == 1
        return data["items"][0]

    @classmethod
    def verify_url_click(cls, request_context: APIRequestContext, url: str):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.VERIFY_URL_CLICK.value,
            data={"url": url},
        )

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
    def campaign(cls, request_context: APIRequestContext, campaign: CampaignModel):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.CAMPAIGN.value,
            data={
                "campaign_name": campaign.name,
                "attack_info_id": campaign.attack_info_id,
                "days_until_fail": campaign.days_until_fail,
                "employees": campaign.employees,
                "attack_url": campaign.attack_url,
                "attack_date": campaign.attack_date,
                "custom_reminder": campaign.custom_reminder,
                "content_id": campaign.content_id,
                "special": campaign.special,
                "company_id": campaign.company_id,
            },
        )

    @classmethod
    def get_attack_execution(cls, request_context: APIRequestContext, id):
        return request_context.get(
            PSApi.API_VERSION.value + PSApi.GET_ATTACK_EXECUTION.value,
            params={"id": id},
        )
