from enum import Enum
from typing import List
from playwright.sync_api import APIRequestContext


class AdminApi(Enum):
    API_VERSION = "/api"

    CAMPAIGN = "/admin/campaign"


class AdminService:
    @classmethod
    def campaign(
        cls,
        request_context: APIRequestContext,
        campaign_name: str,
        attack_info_id: str,
        days_until_fail: int,
        employees: List[str],
        company_id: int = None,  # not needed for customer admin
    ):
        return request_context.post(
            AdminApi.API_VERSION.value + AdminApi.CAMPAIGN.value,
            data={
                "campaign_name": campaign_name,
                "attack_info_id": attack_info_id,
                "days_until_fail": days_until_fail,
                "employees": employees,
                "attack_url": None,
                "attack_date": None,
                "custom_reminder": None,
                "content_id": None,
                "special": [],
                "company_id": company_id,
            },
        )
