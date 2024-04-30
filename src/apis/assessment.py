from enum import Enum
from playwright.sync_api import APIRequestContext
import allure


class AddinApi(Enum):
    API_VERSION = "/api"

    INFO = "/assessment/info"
    ASSESSMENT = "/assessment/assessment"
    INCIDENT = "/assessment/incident"
    ASSESSMENT_REPORT = "/assessment/assessment_report"


class AssessmentService:
    @classmethod
    @allure.step("AssessmentService: get company assessment service info")
    def info(cls, request_context: APIRequestContext):
        return request_context.get(AddinApi.API_VERSION.value + AddinApi.INFO.value)

    @classmethod
    @allure.step("AssessmentService: assess a mail")
    def assessment(cls, request_context: APIRequestContext, mime_content: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={"mime_content": mime_content},
        )

    @classmethod
    @allure.step("AssessmentService: get assessesment by id")
    def assessment_by_id(cls, request_context: APIRequestContext, id: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={"id": id},
        )

    @classmethod
    @allure.step("AssessmentService: report an incident")
    def incident(cls, request_context: APIRequestContext, mime_content: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.INCIDENT.value,
            data={"mime_content": mime_content},
            timeout=60 * 1000,
        )

    @classmethod
    @allure.step("AssessmentService: report an assessment with no mail")
    def assessment_report(
        cls,
        request_context: APIRequestContext,
        message_text: str,
        sender_address: str,
    ):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={
                "message_text": message_text,
                "sender_address": sender_address,
            },
        )

    @classmethod
    @allure.step("AssessmentService: report by aironworks id")
    def assessment_report_aironworks_id(
        cls,
        request_context: APIRequestContext,
        aironworks_id: str,
    ):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={
                "aironworks_id": aironworks_id,
            },
        )

    @classmethod
    @allure.step("AssessmentService: get assessesment report by id")
    def assessment_report_by_id(cls, request_context: APIRequestContext, id: str):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={"id": id},
        )
