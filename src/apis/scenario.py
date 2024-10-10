import time
from dataclasses import asdict
from datetime import datetime, timedelta

import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.base_service import BaseService
from src.apis.psapi import PSApi
from src.models.scenario.list_attack_infos_model import ListAttackInfosModel
from src.models.simulation_campaign.simulation_campaign_urls import CampaignUrls


class ScenarioService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('ScenarioService: post list attack infos {list_attack_infos}')
    def post_list_attack_infos(
        self, list_attack_infos: ListAttackInfosModel
    ) -> APIResponse:
        return self._post(
            PSApi.LIST_ATTACK_INFOS.get_endpoint(), data=asdict(list_attack_infos)
        )

    @allure.step('ScenarioService: get attack infos {scenario_id}')
    def get_attack_info(self, scenario_id: str) -> APIResponse:
        return self._get(
            PSApi.GET_ATTACK_INFO.get_endpoint(), params={'id': f'{scenario_id}'}
        )

    @allure.step('ScenarioService: get list domains')
    def get_list_domains(self, include_all: bool) -> APIResponse:
        params = {'include_all': f'{include_all}'}
        return self._get(PSApi.LIST_DOMAINS.get_endpoint(), params=params)

    @allure.step('ScenarioService: get attack tags')
    def get_attack_tags(self) -> APIResponse:
        return self._get(PSApi.GET_ATTACK_TAGS.get_endpoint())

    @allure.step(
        'ScenarioService: aw admin get campaign urls {campaign_id} campaign_id'
    )
    def aw_admin_campaign_urls(
        self, campaign_id: int, wait_time: int = 100
    ) -> CampaignUrls:
        start_time = datetime.now()
        while True:
            response = self._get(
                PSApi.ADMIN_CAMPAIGN_ATTACK_URLS.get_endpoint().format(
                    campaign_id=campaign_id
                )
            )
            assert response.ok, f'{response.json()=}'
            campaign_urls = CampaignUrls.from_dict(response.json())

            if campaign_urls.attacks[0].status in [
                'COMPLETED',
                'ONGOING',
            ] or datetime.now() - start_time > timedelta(seconds=wait_time):
                break
            time.sleep(1)
        return campaign_urls
