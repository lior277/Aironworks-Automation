from playwright.sync_api import APIRequestContext
from src.models.education_campaign_model import EducationCampaignModel
from .psapi import PSApi
import allure
from dataclasses import asdict


class EducationService:
    @classmethod
    @allure.step("EducationService: start an education campaign")
    def campaign(
        cls, request_context: APIRequestContext, campaign: EducationCampaignModel
    ):
        return request_context.post(
            PSApi.API_VERSION.value + PSApi.EDUCATION_CAMPAIGN.value,
            data=asdict(campaign),
        )
