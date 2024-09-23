from dataclasses import asdict

import allure
from playwright.sync_api import APIRequestContext, APIResponse, expect

from ..models.company.employee_delete_model import EmployeeDeleteModel
from ..models.company.employee_list_ids_model import EmployeeListIdsModel
from ..models.company.employee_update_model import EmployeeUpdateModel
from ..models.company.patch_localized_configs_model import PatchLocalizedConfigsModel
from .base_service import BaseService
from .psapi import PSApi


class CompanyService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('CompanyService: create employees')
    def create_employees(self, file_path: str, overwrite: bool = False) -> APIResponse:
        return self._post(
            PSApi.UPLOAD_EMPLOYEE_INFO.get_endpoint(),
            data={'file_path': file_path, 'overwrite': overwrite},
        )

    @allure.step('CompanyService: get create employees status')
    def create_employees_status(self, op_id: str) -> APIResponse:
        return self._get(
            PSApi.UPLOAD_EMPLOYEE_INFO_STATUS.get_endpoint().format(op_id=op_id)
        )

    @allure.step('CompanyService: get company config')
    def localized_config(self) -> APIResponse:
        return self._get(PSApi.COMPANY_LOCALIZED_CONFIG.get_endpoint())

    @allure.step('CompanyService: get employee count')
    def employee_count(self) -> APIResponse:
        return self._get(PSApi.COMPANY_EMPLOYEE_COUNT.get_endpoint())

    @allure.step('CompanyService: update company config')
    def patch_localized_config(
        self, language: str, localized_configs_model: PatchLocalizedConfigsModel
    ) -> APIResponse:
        return self._patch(
            PSApi.COMPANY_LOCALIZED_CONFIG_LANGUAGE.get_endpoint().format(
                language=language
            ),
            data=asdict(localized_configs_model),
        )

    @allure.step('CompanyService: get employee by {email} mail')
    def employee_by_mail(self, email: str) -> APIResponse:
        result = self._post(
            PSApi.EMPLOYEE_LIST.get_endpoint(),
            data={
                'employee_role': True,
                'filters': {
                    'items': [
                        {
                            'columnField': 'email',
                            'operatorValue': 'contains',
                            'id': 0,
                            'value': email,
                        }
                    ],
                    'linkOperator': 'and',
                    'quickFilterValues': [],
                    'quickFilterLogicOperator': 'and',
                },
                'offset': 0,
                'limit': 1,
                'sorting': [],
            },
        )
        expect(result).to_be_ok()
        data = result.json()
        assert 'items' in data
        assert len(data['items']) == 1
        return data['items'][0]

    @allure.step('CompanyService: get employee list')
    def get_employee_list(self, total: int = 15, filters=None) -> APIResponse:
        payload = {
            'employee_role': True,
            'filters': filters,
            'limit': total,
            'offset': 0,
            'sorting': [],
        }
        return self._post(PSApi.EMPLOYEE_LIST.get_endpoint(), data=payload)

    @allure.step('CompanyService: get employee ids')
    def get_employee_ids(self, employee_ids: EmployeeListIdsModel) -> APIResponse:
        return self._post(
            PSApi.EMPLOYEE_LIST_IDS.get_endpoint(), data=asdict(employee_ids)
        )

    @allure.step('CompanyService: delete employees')
    def delete_employees(self, employees: EmployeeDeleteModel) -> APIResponse:
        return self._post(PSApi.EMPLOYEE_DELETE.get_endpoint(), data=asdict(employees))

    @allure.step('CompanyService: update employees')
    def update_employees(self, employees: EmployeeUpdateModel) -> APIResponse:
        return self._post(PSApi.EMPLOYEE_UPDATE.get_endpoint(), data=asdict(employees))
