import os
from datetime import datetime

from src.configs.config_loader import AppFolders
from src.page_objects.content_library import ContentType


class ContentLibraryEntity:
    def __init__(
        self,
        content_type: ContentType,
        title: str,
        sensitive_information: bool,
        topic: str,
        url: str = None,
        pdf_file_path: str = None,
    ):
        self.content_type = content_type
        self.title = title
        self.sensitive_information = sensitive_information
        self.topic = topic
        self.url = url
        self.pdf_file_path = pdf_file_path


class ContentLibraryEntityFactory:
    @staticmethod
    def get_video_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.VIDEO,
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            sensitive_information=False,
            url='https://www.youtube.com/watch?v=nDZbgmSmJBg',
            topic='e2e Admin Topic - Video',
        )

    @staticmethod
    def get_pdf_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.PDF,
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            sensitive_information=False,
            pdf_file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.pdf'),
            topic='e2e Admin Topic - PDF',
        )

    @staticmethod
    def get_slides_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.SLIDES,
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            sensitive_information=False,
            url='https://docs.google.com/presentation/d/1MXg2I9fVtFhFJaRwI857VN8McO5PhsNZaQnsBgY3uH0/edit?usp=sharing',
            topic='e2e Admin Topic - Slides',
        )
