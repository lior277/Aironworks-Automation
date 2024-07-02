import time
from dataclasses import asdict
from datetime import datetime, timedelta

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.psapi import PSApi
from src.models.scenario.list_attack_infos_model import ListAttackInfosModel
from src.models.simulation_campaign.simulation_campaign_urls import CampaignUrls


class ScenarioService:
    @classmethod
    @allure.step("ScenarioService: post list attack infos")
    def post_list_attack_infos(
        cls, request_context: APIRequestContext, list_attack_infos: ListAttackInfosModel
    ) -> APIResponse:
        return request_context.post(
            PSApi.LIST_ATTACK_INFOS.get_endpoint(), data=asdict(list_attack_infos)
        )

    @classmethod
    @allure.step("ScenarioService: get attack infos")
    def get_attack_info(
        cls, request_context: APIRequestContext, scenario_id: str
    ) -> APIResponse:
        return request_context.get(
            PSApi.GET_ATTACK_INFO.get_endpoint(), params={"id": f"{scenario_id}"}
        )

    @classmethod
    @allure.step("ScenarioService: aw admin get campaign urls")
    def aw_admin_campaign_urls(
        cls, request_context: APIRequestContext, campaign_id: int, wait_time: int = 100
    ) -> CampaignUrls:
        start_time = datetime.now()
        while True:
            response = request_context.get(
                PSApi.ADMIN_CAMPAIGN_ATTACK_URLS.get_endpoint().format(
                    campaign_id=campaign_id
                )
            )
            assert response.ok, f"{response.json()=}"
            campaign_urls = CampaignUrls.from_dict(response.json())

            if campaign_urls.attacks[0].status in [
                "COMPLETED",
                "ONGOING",
            ] or datetime.now() - start_time > timedelta(seconds=wait_time):
                break
            time.sleep(1)
        return campaign_urls
