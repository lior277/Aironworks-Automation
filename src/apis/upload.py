import os
from collections import OrderedDict
from typing import Literal

import allure
from playwright.sync_api import APIRequestContext, APIResponse, FilePayload, expect

from .base_service import BaseService
from .psapi import PSApi


class UploadService(BaseService):
    def __init__(self, request_context: APIRequestContext):
        super().__init__(request_context)

    @allure.step('UploadService: upload file api')
    def upload_file_api(
        self, path: str, name: str, kind: Literal['LOGO', 'ATTACHMENT', 'TEMPORARY']
    ) -> APIResponse:
        return self._post(
            PSApi.UPLOAD_URL.get_endpoint(),
            data={'path': path, 'name': name, 'kind': kind},
        )

    @allure.step('UploadService: upload file api')
    def upload_file(
        self,
        path: str,
        type: str,
        data: str,
        kind: Literal['LOGO', 'ATTACHMENT', 'TEMPORARY'],
    ) -> APIResponse:
        name = os.path.basename(path)
        response = self._post(
            PSApi.UPLOAD_URL.get_endpoint(), data={'name': name, 'kind': kind}
        )
        expect(response).to_be_ok()
        upload_url = response.json()['url']
        upload_fields = response.json()['fields']
        multipart_data = OrderedDict(upload_fields)
        multipart_data['Content-Type'] = type
        multipart_data['file'] = FilePayload(buffer=data, mimeType=type, name=name)
        s3_upload = self._post(upload_url, multipart=multipart_data)

        expect(s3_upload).to_be_ok()
        return response.json()['path']
