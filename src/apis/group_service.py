import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.base_service import BaseService
from src.apis.psapi import PSApi


class GroupService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('GroupService: get group list')
    def get_group_list(self) -> APIResponse:
        return self._get(PSApi.GROUPS_LIST.get_endpoint())

    @allure.step('GroupService: delete group by {group_id} id')
    def delete_group(self, group_id: str) -> APIResponse:
        return self._post(
            PSApi.DELETE_GROUP.get_endpoint(), data={'group_id': f'{group_id}'}
        )
