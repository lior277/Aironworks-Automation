from enum import Enum
from typing import List
from playwright.sync_api import APIRequestContext, expect
from csv import DictWriter
import io
from base64 import b64encode


class CompanyApi(Enum):
    API_VERSION = "/api"

    UPLOAD_EMPLOYEE_INFO = "/company/upload_employee_info"
    EMPLOYEE_LIST = "/company/employee_list"


class CompanyService:
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
            CompanyApi.API_VERSION.value + CompanyApi.UPLOAD_EMPLOYEE_INFO.value,
            data={
                "file_path": "random_path.csv",
                "file_text": data,
                "overwrite": False,
            },
        )

    @classmethod
    def employee_by_mail(cls, request_context: APIRequestContext, email: str):
        result = request_context.post(
            CompanyApi.API_VERSION.value + CompanyApi.EMPLOYEE_LIST.value,
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
