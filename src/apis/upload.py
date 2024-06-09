from dataclasses import asdict
import os
from typing import Literal
import allure
from playwright.sync_api import APIRequestContext, FilePayload, APIResponse, expect

from src.models.auth.signup_model import EmailSignupModel
from src.models.auth.user_model import UserModel
from .psapi import PSApi
from collections import OrderedDict


class UploadService:
    @classmethod
    @allure.step("UploadService: upload file api")
    def upload_file_api(
        cls,
        request_context: APIRequestContext,
        path: str,
        name: str,
        kind: Literal["LOGO", "ATTACHMENT", "TEMPORARY"],
    ) -> APIResponse:
        return request_context.post(
            PSApi.UPLOAD_URL.get_endpoint(),
            data={
                "path": path,
                "name": name,
                "kind": kind,
            },
        )

    @classmethod
    @allure.step("UploadService: upload file api")
    def upload_file(
        cls,
        request_context: APIRequestContext,
        path: str,
        type: str,
        data: str,
        kind: Literal["LOGO", "ATTACHMENT", "TEMPORARY"],
    ) -> APIResponse:
        name = os.path.basename(path)
        response = request_context.post(
            PSApi.UPLOAD_URL.get_endpoint(),
            data={
                "name": name,
                "kind": kind,
            },
        )
        expect(response).to_be_ok()
        upload_url = response.json()["url"]
        upload_fields = response.json()["fields"]
        multipart_data = OrderedDict(upload_fields)
        multipart_data["Content-Type"] = type
        multipart_data["file"] = FilePayload(buffer=data, mimeType=type, name=name)
        s3_upload = request_context.post(
            upload_url,
            multipart=multipart_data,
        )

        expect(s3_upload).to_be_ok()
        return response.json()["path"]
