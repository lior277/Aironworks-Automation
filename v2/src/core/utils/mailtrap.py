import os
import tempfile
import time
import zipfile
from datetime import datetime
from email import message_from_bytes
from email.message import Message
from xml.etree import ElementTree as ET

import allure
import fitz
from playwright.sync_api import APIRequestContext, Playwright, expect

from src.configs.config_loader import AppConfigs
from src.models.mait_trap_model import MailTrapModel
from src.utils.log import Log, print_execution_time


def find_attachment(content_type: str = 'application/octet-stream'):
    def predicate(mailtrap: MailTrap, mail):
        mail_id = mail['id']
        mail_raw = mailtrap.raw_message(
            AppConfigs.MAILTRAP_ASSESSMENT_INBOX_ID, mail_id
        )

        message: Message = message_from_bytes(mail_raw.body())
        parts = message.get_payload()
        for attachment in parts:
            if attachment.get_filename() is not None:
                if attachment.get_content_type() == content_type:
                    return True
        return False

    return predicate


def find_email(email, subject=None):
    def predicate(_, mail):
        result = mail['to_email'] == email
        if subject is not None:
            result = result and mail['subject'] == subject
        return result

    return predicate


class MailTrap:
    def __init__(
        self,
        playwright: Playwright,
        base_url='https://mailtrap.io',
        account_id=AppConfigs.MAILTRAP_ACCOUNT_ID,
    ):
        headers = {'Api-Token': AppConfigs.MAILTRAP_API_TOKEN}
        self.request_context: APIRequestContext = playwright.request.new_context(
            base_url=base_url, extra_http_headers=headers
        )
        self._account_id = account_id

    def messages(self, inbox_id, page: int = None, email_to: str = None):
        params = {}
        if email_to:
            params.update({'search': f'{email_to}'})
        if page:
            params.update({'page': page})
        response = self.request_context.get(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages',
            params=params,
        )
        expect(response).to_be_ok()
        return response

    def inbox_attributes(self, inbox_id):
        params = {}
        response = self.request_context.get(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}', params=params
        )
        expect(response).to_be_ok()
        return response

    def raw_message(self, inbox_id, message_id):
        response = self.request_context.get(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}/body.raw'
        )
        expect(response).to_be_ok()
        return response

    def message_source(self, inbox_id, message_id):
        response = self.request_context.get(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}/body.htmlsource'
        )
        expect(response).to_be_ok()
        return response

    def delete_message(
        self, message_id, inbox_id: str = AppConfigs.PERF_EMPLOYEE_INBOX_ID
    ):
        response = self.request_context.delete(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}/messages/{message_id}'
        )
        expect(response).to_be_ok()
        return response

    def clean_inbox(self, inbox_id):
        response = self.request_context.patch(
            f'/api/accounts/{self._account_id}/inboxes/{inbox_id}/clean'
        )
        expect(response).to_be_ok()

    def clean_inboxes(self, list_mail_traps: list[MailTrapModel]):
        for mail in list_mail_traps:
            response = self.request_context.patch(
                f'/api/accounts/{self._account_id}/inboxes/{mail.id}/clean'
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
                    self.delete_message(inbox_id, get_mails.json()[0]['id'])
                return get_mails.json()[0]
            time.sleep(1)
            if (datetime.now() - start_time).seconds > timeout:
                return None

    @print_execution_time
    def wait_for_mails(
        self, inbox_id: str = AppConfigs.PERF_EMPLOYEE_INBOX_ID, timeout: int = 600
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
                if email['to_email'] in employees_email_list:
                    employees_email_list.remove(email['to_email'])
                    self.delete_message(email['id'])
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
                Log.info(f'Checking {mail_trap.id}')
                attributes = self.inbox_attributes(mail_trap.id)
                if attributes.json()['emails_count'] < emails_per_inbox:
                    Log.info(f'not enough mails received {mail_trap.id}')
                    continue
                page = 0
                while True:
                    page += 1  # 1 is the first page
                    emails = self.messages(inbox_id=mail_trap.id, page=page)
                    Log.info(f'Checking page {page} in {mail_trap.id}')
                    if emails.json():
                        for email in emails.json():
                            if email['to_email'] in employees_email_list:
                                employees_email_list.remove(email['to_email'])
                                if remove_messages:
                                    try:
                                        self.delete_message(
                                            inbox_id=mail_trap.id,
                                            message_id=email['id'],
                                        )
                                    except Exception:
                                        Log.info(
                                            f"Unable to delete {email['id']=} in {mail_trap.id=}"
                                        )
                    else:
                        break
                Log.info(f'{len(employees_email_list)} left to check')
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

    @allure.step('Download attachments with file paths')
    def download_attachments_with_file_paths(
        self, inbox_id: str, emails: list, content_type: str, timeout: int = 120
    ) -> list[str]:
        # Wait for an email with the desired attachment
        filepaths = []
        for email in emails:
            filepath = self.download_attachment(
                inbox_id, email, content_type, timeout=timeout
            )
            filepaths.append(filepath)
        return filepaths

    @allure.step('Extract links')
    def extract_links(self, filepaths: list) -> list[str]:
        check_links = []
        for filepath in filepaths:
            print('Opening file:', filepath)
            if filepath.endswith('.pdf'):
                # Extract links from PDF using PyMuPDF
                pdf_document = fitz.open(filepath)
                links = []
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)
                    for link in page.get_links():
                        if 'uri' in link:
                            links.append(link['uri'])

                # Open the first link (or handle multiple links as needed)
                if links:
                    print(f'Add link: {links[1]}')
                    check_links.append(links[1])
                else:
                    assert False, 'No links found in the PDF.'

            # Handle DOCX files

            elif filepath.endswith('.docx'):
                # Extract links from DOCX using python-docx
                with zipfile.ZipFile(filepath, 'r') as docx:
                    rels_xml = docx.read('word/_rels/document.xml.rels')
                    rels_tree = ET.XML(rels_xml)

                    # Extract hyperlinks (which are stored as 'Relationship' entries with a 'Target' attribute)
                    for rel in rels_tree.findall(
                        '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'
                    ):
                        if (
                            rel.attrib.get('Type')
                            == 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject'
                        ):
                            link = rel.attrib.get('Target')
                            print(f'Add link: {link}')
                            if link:
                                check_links.append(link)

                if not check_links:
                    assert False, 'No links found in the DOCX.'
            os.remove(filepath)
        return check_links

    def download_attachment(
        self, inbox_id: str, email: str, content_types: str, timeout: int = 120
    ):
        # Wait for an email with the desired attachment
        mail = self.wait_for_mail(
            inbox_id=inbox_id, predicate=find_email(email), timeout=timeout
        )
        assert mail is not None, (
            f'Unable to find email {email} please check the mailtrap inbox {inbox_id}'
        )

        # Get raw message
        mail_raw = self.raw_message(inbox_id, mail['id'])
        message = message_from_bytes(mail_raw.body())
        parts = message.get_payload()

        # Process each part to find the attachment
        for part in parts:
            print('Content:', part.get_content_type())
            if part.get_content_type() in content_types and part.get_filename():
                attachment_content = part.get_payload(decode=True)
                original_name = part.get_filename()
                extension = os.path.splitext(original_name)[1]
                with tempfile.NamedTemporaryFile(
                    mode='wb', suffix=extension, delete=False
                ) as temp_file:
                    temp_file.write(attachment_content)
                    file_name = temp_file.name
                    temp_filepath = file_name
                return temp_filepath
        return None

    def check_custom_header(
        self, inbox_id: str, email: str, header_key: str, header_value: str, timeout=120
    ):
        # Retrieve the raw email source
        mail = self.wait_for_mail(
            inbox_id=inbox_id, predicate=find_email(email), timeout=timeout
        )
        assert mail is not None, (
            f'Unable to find email {email} please check the mailtrap inbox {inbox_id}'
        )
        # Get raw message
        mail_raw = self.raw_message(inbox_id, mail['id'])
        message = message_from_bytes(mail_raw.body())
        parts = message.get_payload()
        text = '{header_key}: {header_value}'
        for part in parts:
            if text in part:
                print(f"Header '{header_key}' with value '{header_value}' found.")
                return True
        print(f"Header '{header_key}' with value '{header_value}' not found.")
        return False

    def close(self):
        pass
        # self.request_context.dispose() removed due to https://github.com/microsoft/playwright/issues/27048 which wasn't fixed for python
