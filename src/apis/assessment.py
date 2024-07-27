from enum import Enum

import allure
from playwright.sync_api import APIRequestContext

from src.apis.base_service import BaseService


class AddinApi(Enum):
    API_VERSION = '/api'

    INFO = '/assessment/info'
    ASSESSMENT = '/assessment/assessment'
    INCIDENT = '/assessment/incident'
    ASSESSMENT_REPORT = '/assessment/assessment_report'


class AssessmentService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('AssessmentService: get company assessment service info')
    def info(self):
        return self._get(AddinApi.API_VERSION.value + AddinApi.INFO.value)

    @allure.step('AssessmentService: assess a mail {mime_content} mime_content')
    def assessment(self, mime_content: str = None):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={'mime_content': mime_content},
        )

    @allure.step('AssessmentService: get assessment by {assessment_id} id')
    def assessment_by_id(self, assessment_id: str = None):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT.value,
            data={'id': assessment_id},
        )

    @allure.step('AssessmentService: report an incident')
    def incident(self, mime_content: str = None):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.INCIDENT.value,
            data={'mime_content': mime_content},
            timeout=60 * 1000,
        )

    @allure.step(
        'AssessmentService: report an assessment with no mail {sender_address} sender address'
    )
    def assessment_report(
        self, message_text: str, sender_address: str, subject: str = None
    ):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={
                'message_text': message_text,
                'sender_address': sender_address,
                'subject': subject,
            },
        )

    @allure.step('AssessmentService: report by {aironworks_id} aironworks id')
    def assessment_report_aironworks_id(self, aironworks_id: str):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={'aironworks_id': aironworks_id},
        )

    @allure.step('AssessmentService: get assessment report by {assessment_id} id')
    def assessment_report_by_id(self, assessment_id: str):
        return self._post(
            AddinApi.API_VERSION.value + AddinApi.ASSESSMENT_REPORT.value,
            data={'id': assessment_id},
        )
