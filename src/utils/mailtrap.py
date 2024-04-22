from src.configs.config_loader import AppConfigs
from playwright.sync_api import Playwright, APIRequestContext, expect
from email import message_from_bytes
from email.message import Message
from datetime import datetime
from base64 import b64decode
import time


def find_attachment(attachment_content):
    def predicate(mailtrap: MailTrap, mail):
        mail_id = mail["id"]
        mail_raw = mailtrap.raw_message(
            AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID, mail_id
        )

        message: Message = message_from_bytes(mail_raw.body())
        parts = message.get_payload()
        data = None
        for attachment in parts:
            if attachment.get_filename() is not None:
                for attach in attachment.get_payload():
                    data = b64decode(attach.as_string())

        if data == attachment_content:
            return True
        return False

    return predicate


def find_email(email):
    def predicate(_, mail):
        return mail["to_email"] == email

    return predicate


class MailTrap:
    def __init__(
        self,
        playwright: Playwright,
        base_url="https://mailtrap.io",
        account_id=AppConfigs.MAILTRAP_ACCOUNT_ID,
    ):
        headers = {"Api-Token": AppConfigs.MAILTRAP_API_TOKEN}
        self.request_context: APIRequestContext = playwright.request.new_context(
            base_url=base_url, extra_http_headers=headers
        )
        self._account_id = account_id

    def messages(self, inbox_id):
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages"
        )
        expect(response).to_be_ok()
        return response

    def raw_message(self, inbox_id, message_id):
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}/body.raw"
        )
        expect(response).to_be_ok()
        return response

    def wait_for_mail(self, inbox_id, predicate, timeout=120):
        start_time = datetime.now()
        while True:
            get_mails = self.messages(inbox_id)

            for mail in get_mails.json():
                if predicate(self, mail):
                    return mail
            time.sleep(1)
            if (datetime.now() - start_time).seconds > timeout:
                return None

    def close(self):
        self.request_context.dispose()
