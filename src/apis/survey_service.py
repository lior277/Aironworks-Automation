import allure
from playwright.sync_api import APIRequestContext, APIResponse

from src.apis.psapi import PSApi
from src.models.survey.add_survey_modal import AddSurveyModel


class SurveyService:

    @classmethod
    @allure.step("SurveyService: get list of surveys")
    def get_list_surveys(cls, request_context: APIRequestContext) -> APIResponse:
        return request_context.get(PSApi.LIST_SURVEYS.get_endpoint())

    @classmethod
    @allure.step("SurveyService: add survey")
    def add_survey(cls, request_context: APIRequestContext, survey: AddSurveyModel) -> APIResponse:
        return request_context.post(PSApi.ADD_SURVEY.get_endpoint(), data=survey.to_filtered_dict())

    @classmethod
    @allure.step("SurveyService: set default survey")
    def set_default_survey(cls, request_context: APIRequestContext, survey_id: AddSurveyModel,
                           value: bool = True) -> APIResponse:
        data = {"id": f"{survey_id}", "value": f"{value}"}
        return request_context.post(PSApi.SET_DEFAULT_SURVEY.get_endpoint(), data=data)

    @classmethod
    @allure.step("SurveyService: delete {2} survey")
    def delete_survey(cls, request_context: APIRequestContext, survey_id: str) -> APIResponse:
        return request_context.post(PSApi.DELETE_SURVEY.get_endpoint(), data={"survey_id": f"{survey_id}"})
