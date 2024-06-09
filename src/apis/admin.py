from playwright.sync_api import APIRequestContext
from src.models.campaign_model import CampaignModel
from .psapi import PSApi
from src.configs.config_loader import AppConfigs
import os


class AdminService:
    @classmethod
    def campaign(cls, request_context: APIRequestContext, campaign: CampaignModel):
        return request_context.post(
            PSApi.CAMPAIGN.get_endpoint(),
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
            PSApi.GET_ATTACK_EXECUTION.get_endpoint(),
            params={"id": id},
        )

    @classmethod
    def company_count(cls, request_context: APIRequestContext):
        return request_context.get(PSApi.COMPANY_COUNT.get_endpoint())
