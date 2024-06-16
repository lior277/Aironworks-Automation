import time
from base64 import b64decode
from datetime import datetime
from email import message_from_bytes
from email.message import Message

from playwright.sync_api import Playwright, APIRequestContext, expect

from src.configs.config_loader import AppConfigs
from src.models.mait_trap_model import MailTrapModel
from src.utils.log import print_execution_time, Log


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


def find_email(email, subject=None):
    def predicate(_, mail):
        result = mail["to_email"] == email
        if subject is not None:
            result = result and mail["subject"] == subject
        return result

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

    def messages(self, inbox_id, page: int = None, email_to: str = None):
        params = {}
        if email_to:
            params.update({"search": f"{email_to}"})
        if page:
            params.update({"page": page})
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages",
            params=params,
        )
        expect(response).to_be_ok()
        return response

    def inbox_attributes(self, inbox_id):
        params = {}
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}",
            params=params,
        )
        expect(response).to_be_ok()
        return response

    def raw_message(self, inbox_id, message_id):
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}/body.raw"
        )
        expect(response).to_be_ok()
        return response

    def message_source(self, inbox_id, message_id):
        response = self.request_context.get(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}/body.htmlsource"
        )
        expect(response).to_be_ok()
        return response

    def delete_message(
        self, message_id, inbox_id: str = AppConfigs.PERF_EMPLOYEE_INBOX_ID
    ):
        response = self.request_context.delete(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}"
        )
        expect(response).to_be_ok()
        return response

    def clean_inbox(self, inbox_id):
        response = self.request_context.patch(
            f"/api/accounts/{self._account_id}/inboxes/{inbox_id}/clean"
        )
        expect(response).to_be_ok()

    def clean_inboxes(self, list_mail_traps: list[MailTrapModel]):
        for mail in list_mail_traps:
            response = self.request_context.patch(
                f"/api/accounts/{self._account_id}/inboxes/{mail.id}/clean"
            )
            expect(response).to_be_ok()

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

    @print_execution_time
    def wait_for_mail_to(
        self, inbox_id, email_to: str, timeout: int = 120, delete_message: bool = False
    ):
        start_time = datetime.now()
        while True:
            get_mails = self.messages(inbox_id, email_to=email_to)
            if get_mails.json():
                if delete_message:
                    self.delete_message(inbox_id, get_mails.json()[0]["id"])
                return get_mails.json()[0]
            time.sleep(1)
            if (datetime.now() - start_time).seconds > timeout:
                return None

    @print_execution_time
    def wait_for_mails(
        self, inbox_id: str = AppConfigs.PERF_EMPLOYEE_INBOX_ID, timeout: int = 120
    ):
        start_time = datetime.now()
        while True:
            get_mails = self.messages(inbox_id)
            if get_mails.json():
                return get_mails.json()
            time.sleep(1)
            if (datetime.now() - start_time).seconds > timeout:
                return None

    @print_execution_time
    def wait_for_all_mail(self, employees_email_list: list[str], timeout: int = 7200):
        start_time = datetime.now()
        while len(employees_email_list) > 0:
            emails = self.wait_for_mails(timeout=600)
            for email in emails:
                if email["to_email"] in employees_email_list:
                    employees_email_list.remove(email["to_email"])
                    self.delete_message(email["id"])
            if (
                len(employees_email_list) == 0
                or (datetime.now() - start_time).seconds > timeout
            ):
                break
        return employees_email_list

    @print_execution_time
    def wait_for_all_mail_in_diff_inboxes(
        self,
        employees_email_list: set[str],
        list_mail_traps: list[MailTrapModel],
        emails_per_inbox,
        remove_messages: bool = False,
        timeout: int = 7200,
    ):
        start_time = datetime.now()
        list_mail_traps = set(list_mail_traps)
        while len(employees_email_list) > 0:
            to_be_removed = set()
            for mail_trap in list_mail_traps:
                Log.info(f"Checking {mail_trap.id}")
                attributes = self.inbox_attributes(mail_trap.id)
                if attributes.json()["emails_count"] < emails_per_inbox:
                    Log.info(f"not enough mails received {mail_trap.id}")
                    continue
                page = 0
                while True:
                    page += 1  # 1 is the first page
                    emails = self.messages(inbox_id=mail_trap.id, page=page)
                    Log.info(f"Checking page {page} in {mail_trap.id}")
                    if emails.json():
                        for email in emails.json():
                            if email["to_email"] in employees_email_list:
                                employees_email_list.remove(email["to_email"])
                                if remove_messages:
                                    try:
                                        self.delete_message(
                                            inbox_id=mail_trap.id,
                                            message_id=email["id"],
                                        )
                                    except Exception:
                                        Log.info(
                                            f"Unable to delete {email['id']=} in {mail_trap.id=}"
                                        )
                    else:
                        break
                Log.info(f"{len(employees_email_list)} left to check")
                if (
                    len(employees_email_list) == 0
                    or (datetime.now() - start_time).seconds > timeout
                ):
                    break
                time.sleep(2)
                to_be_removed.add(mail_trap)
            for mail_trap in to_be_removed:
                list_mail_traps.remove(mail_trap)
        return employees_email_list

    def close(self):
        pass
        # self.request_context.dispose() removed due to https://github.com/microsoft/playwright/issues/27048 which wasn't fixed for python
