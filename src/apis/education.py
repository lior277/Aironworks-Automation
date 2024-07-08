import time
from dataclasses import asdict
from datetime import datetime, timedelta

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.models.education_campaign_model import EducationCampaignModel, EducationCampaignStatus
from .base_service import BaseService
from .psapi import PSApi
from ..models.education.education_assignments import EducationAssignmentsModel


class EducationService(BaseService):

    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step("EducationService: start an education campaign")
    def start_campaign(self, campaign: EducationCampaignModel) -> APIResponse:
        return self._post(PSApi.EDUCATION_CAMPAIGN.get_endpoint(), data=asdict(campaign))

    @allure.step("EducationService: get education campaign details")
    def get_campaign_details(self, campaign_id: str) -> APIResponse:
        return self._get(PSApi.EDUCATION_CAMPAIGN_DETAILS.get_endpoint().format(campaign_id=campaign_id))

    @allure.step("EducationService: delete education campaign")
    def delete_education_campaign(self, campaign_id: str) -> APIResponse:
        return self._delete(PSApi.EDUCATION_CAMPAIGN_DETAILS.get_endpoint().format(campaign_id=campaign_id))

    @allure.step("EducationService: get education campaign list")
    def get_education_campaign_list(self, offset: int = 0, limit: int = 8,
                                    statuses: list[EducationCampaignStatus] = [EducationCampaignStatus.ONGOING.name,
                                                                               EducationCampaignStatus.PENDING.name]) -> APIResponse:
        data = {"status": statuses, "offset": offset, "limit": limit, "sorting": []}
        return self._post(PSApi.EDUCATION_CAMPAIGN_LIST.get_endpoint(), data=data)

    @allure.step("EducationService: get all education content")
    def get_content_pagination(self, offset: int = 0, limit: int = 6) -> APIResponse:
        params = {"offset": offset, "limit": limit}
        return self._get(PSApi.EDUCATION_CONTENT.get_endpoint(), params=params)

    @allure.step("EducationService: aw admin get education assignments")
    def aw_admin_education_assignments(self, campaign_id: int, wait_time: int = 100) -> APIResponse:
        start_time = datetime.now()
        while True:
            response = self._get(PSApi.ADMIN_EDUCATION_ASSIGNMENTS.get_endpoint().format(campaign_id=campaign_id))
            education_assignments = EducationAssignmentsModel.from_dict(response.json())
            if education_assignments.campaign_status in ['COMPLETED', 'ONGOING'] \
                    and datetime.now() - start_time > timedelta(seconds=wait_time):
                break
            time.sleep(1)
        return response
