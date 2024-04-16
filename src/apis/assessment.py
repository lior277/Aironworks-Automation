from enum import Enum
from playwright.sync_api import APIRequestContext


class AddinApi(Enum):
    API_VERSION = "/api"

    INFO = "/assessment/info"
    ASSESSMENT = "/assessment/assessment"


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
