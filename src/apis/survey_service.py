import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.base_service import BaseService
from src.apis.psapi import PSApi
from src.models.survey.add_survey_modal import AddSurveyModel


class SurveyService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('SurveyService: get list of surveys')
    def get_list_surveys(self) -> APIResponse:
        return self._get(PSApi.LIST_SURVEYS.get_endpoint())

    @allure.step('SurveyService: add survey')
    def add_survey(self, survey: AddSurveyModel) -> APIResponse:
        return self._post(
            PSApi.ADD_SURVEY.get_endpoint(), data=survey.to_filtered_dict()
        )

    @allure.step('SurveyService: set default survey {survey_id}')
    def set_default_survey(
        self, survey_id: AddSurveyModel, value: bool = True
    ) -> APIResponse:
        data = {'id': f'{survey_id}', 'value': f'{value}'}
        return self._post(PSApi.SET_DEFAULT_SURVEY.get_endpoint(), data=data)

    @allure.step('SurveyService: delete {survey_id} survey')
    def delete_survey(self, survey_id: str) -> APIResponse:
        return self._post(
            PSApi.DELETE_SURVEY.get_endpoint(), data={'survey_id': f'{survey_id}'}
        )

    @allure.step('SurveyService: get {survey_id} survey')
    def get_survey(self, survey_id: str) -> APIResponse:
        return self._get(PSApi.GET_SURVEY.get_endpoint(), params={'id': f'{survey_id}'})

    @allure.step('SurveyService: get specific survey answer stats {survey_id}')
    def get_specific_survey_answer_stats(self, survey_id: str) -> APIResponse:
        return self._get(
            PSApi.GET_SPECIFIC_SURVEY_ANSWER_STATS.get_endpoint(),
            params={'survey_id': f'{survey_id}'},
        )
