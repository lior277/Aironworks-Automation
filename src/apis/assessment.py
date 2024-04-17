from enum import Enum
from playwright.sync_api import APIRequestContext


class AddinApi(Enum):
    API_VERSION = "/api"

    INFO = "/assessment/info"
    ASSESSMENT = "/assessment/assessment"
    INCIDENT = "/assessment/incident"
    ASSESSMENT_REPORT = "/assessment/assessment_report"


class AssessmentService:
    @classmethod
    def info(cls, request_context: APIRequestContext):
        return request_context.get(AddinApi.API_VERSION.value + AddinApi.INFO.value)

    @classmethod
    def assessment(cls, request_context: APIRequestContext, mime_content: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={"mime_content": mime_content},
        )

    @classmethod
    def assessment_by_id(cls, request_context: APIRequestContext, id: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={"id": id},
        )

    @classmethod
    def incident(cls, request_context: APIRequestContext, mime_content: str = None):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.INCIDENT.value,
            data={"mime_content": mime_content},
        )

    @classmethod
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
    def assessment_report_by_id(cls, request_context: APIRequestContext, id: str):
        return request_context.post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={"id": id},
        )
