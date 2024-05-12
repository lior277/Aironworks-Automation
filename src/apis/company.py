from playwright.sync_api import APIRequestContext, expect
from src.models.employee_model import EmployeeModel
from csv import DictWriter
import io
from base64 import b64encode
from .psapi import PSApi
import allure


class CompanyService:
    @classmethod
    @allure.step("CompanyService: create employee")
    def create_employee(
        cls, request_context: APIRequestContext, employee: EmployeeModel
    ):
        buffer = io.StringIO()
        writer = DictWriter(buffer, fieldnames=["first_name", "last_name", "email"])
        writer.writerow(
            {"first_name": "First Name", "last_name": "Last Name", "email": "Email"}
        )
        writer.writerow(
            {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
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
    @allure.step("CompanyService: get company config")
    def localized_config(cls, request_context: APIRequestContext):
        return request_context.get(
            PSApi.API_VERSION.value + PSApi.COMPANY_LOCALIZED_CONFIG.value
        )

    @classmethod
    @allure.step("CompanyService: get employee by mail")
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
