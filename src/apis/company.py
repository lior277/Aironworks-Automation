import io
from csv import DictWriter
from dataclasses import asdict

import allure
from playwright.sync_api import APIRequestContext, expect, APIResponse

from src.models.company.employee_model import EmployeeModel
from .psapi import PSApi
from .upload import UploadService
from ..models.company.employee_delete_model import EmployeeDeleteModel
from ..models.company.employee_list_ids_model import EmployeeListIdsModel
from ..models.company.employee_update_model import EmployeeUpdateModel
from ..models.company.patch_localized_configs_model import PatchLocalizedConfigsModel


class CompanyService:
    @classmethod
    @allure.step("CompanyService: create employee")
    def create_employee(
            cls, request_context: APIRequestContext, employee: EmployeeModel
    ) -> APIResponse:
        return cls.create_employees(request_context, [employee], False)

    @classmethod
    @allure.step("CompanyService: create employees")
    def create_employees(
            cls,
            request_context: APIRequestContext,
            employees: list[EmployeeModel],
            overwrite: bool = False,
    ) -> APIResponse:
        buffer = io.StringIO()
        writer = DictWriter(buffer, fieldnames=["first_name", "last_name", "email"])
        writer.writerow(
            {"first_name": "First Name", "last_name": "Last Name", "email": "Email"}
        )
        for employee in employees:
            writer.writerow(
                {
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "email": employee.email,
                }
            )
        buffer.flush()
        buffer.seek(0, 0)
        data = buffer.read().encode("utf-8")
        path = UploadService.upload_file(
            request_context, "employees.csv", "text/csv", data, "TEMPORARY"
        )

        return request_context.post(
            PSApi.UPLOAD_EMPLOYEE_INFO.get_endpoint(),
            data={
                "file_path": path,
                "overwrite": overwrite,
            },
        )

    @classmethod
    @allure.step("CompanyService: get create employees status")
    def create_employees_status(
        cls, request_context: APIRequestContext, op_id: str
    ) -> APIResponse:
        return request_context.get(
            PSApi.UPLOAD_EMPLOYEE_INFO_STATUS.get_endpoint().format(op_id=op_id)
        )

    @classmethod
    @allure.step("CompanyService: get company config")
    def localized_config(cls, request_context: APIRequestContext) -> APIResponse:
        return request_context.get(PSApi.COMPANY_LOCALIZED_CONFIG.get_endpoint())

    @classmethod
    @allure.step("CompanyService: update company config")
    def patch_localized_config(cls, request_context: APIRequestContext, language: str,
                               localized_configs_model: PatchLocalizedConfigsModel) -> APIResponse:
        return request_context.patch(PSApi.COMPANY_LOCALIZED_CONFIG_LANGUAGE.get_endpoint().format(language=language),
                                     data=asdict(localized_configs_model))

    @classmethod
    @allure.step("CompanyService: get employee by mail")
    def employee_by_mail(
            cls, request_context: APIRequestContext, email: str
    ) -> APIResponse:
        result = request_context.post(
            PSApi.EMPLOYEE_LIST.get_endpoint(),
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
    @allure.step("CompanyService: get employee ids")
    def get_employee_ids(
            cls, request_context: APIRequestContext, employee_ids: EmployeeListIdsModel
    ) -> APIResponse:
        return request_context.post(
            PSApi.EMPLOYEE_LIST_IDS.get_endpoint(), data=asdict(employee_ids)
        )

    @classmethod
    @allure.step("CompanyService: delete employees")
    def delete_employees(
            cls, request_context: APIRequestContext, employees: EmployeeDeleteModel
    ) -> APIResponse:
        return request_context.post(
            PSApi.EMPLOYEE_DELETE.get_endpoint(), data=asdict(employees)
        )

    @classmethod
    @allure.step("CompanyService: update employees")
    def update_employees(
            cls, request_context: APIRequestContext, employees: EmployeeUpdateModel
    ) -> APIResponse:
        return request_context.post(
            PSApi.EMPLOYEE_UPDATE.get_endpoint(), data=asdict(employees)
        )
