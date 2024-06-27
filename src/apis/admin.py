from dataclasses import asdict

import allure
from playwright.sync_api import APIRequestContext

from src.models.campaign_model import CampaignModel
from .base_service import BaseService
from .psapi import PSApi


class AdminService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step("create simulation campaign {campaign}")
    def start_campaign(self, campaign: CampaignModel):
        return self._post(PSApi.CAMPAIGN.get_endpoint(), data=asdict(campaign))

    @allure.step("get attack execution {campaign_id}")
    def get_attack_execution(self, campaign_id: str):
        return self._get(PSApi.GET_ATTACK_EXECUTION.get_endpoint(), params={"id": campaign_id})

    @allure.step("get company count")
    def company_count(self):
        return self._get(PSApi.COMPANY_COUNT.get_endpoint())
