import time
from dataclasses import asdict
from datetime import datetime, timedelta

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.models.education_campaign_model import EducationCampaignModel
from .psapi import PSApi
from ..models.education.education_assignments import EducationAssignmentsModel


class EducationService:
    @classmethod
    @allure.step("EducationService: start an education campaign")
    def start_campaign(cls, request_context: APIRequestContext, campaign: EducationCampaignModel) -> APIResponse:
        return request_context.post(PSApi.EDUCATION_CAMPAIGN.get_endpoint(), data=asdict(campaign))

    @classmethod
    @allure.step("EducationService: get all education content")
    def get_content_pagination(cls, request_context: APIRequestContext, offset: int = 0, limit: int = 6) -> APIResponse:
        params = {"offset": offset, "limit": limit}
        return request_context.get(PSApi.EDUCATION_CONTENT.get_endpoint(), params=params)

    @classmethod
    @allure.step("EducationService: aw admin get education assignments")
    def aw_admin_education_assignments(cls, request_context: APIRequestContext, campaign_id: int,
                                       wait_time: int = 100) -> APIResponse:
        start_time = datetime.now()
        while True:
            response = request_context.get(PSApi.ADMIN_EDUCATION_ASSIGNMENTS.get_endpoint()
                                           .format(campaign_id=campaign_id))
            education_assignments = EducationAssignmentsModel.from_dict(response.json())
            if education_assignments.campaign_status in ['COMPLETED', 'ONGOING'] \
                    and datetime.now() - start_time > timedelta(seconds=wait_time):
                break
            time.sleep(1)
        return response
