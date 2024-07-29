from datetime import datetime

from src.page_objects.content_library import ContentType


class ContentLibraryEntity:
    def __init__(
        self,
        content_type: ContentType,
        title: str,
        sensitive_information: bool,
        url: str,
        topic: str,
    ):
        self.content_type = content_type
        self.title = title
        self.sensitive_information = sensitive_information
        self.url = url
        self.topic = topic


class ContentLibraryEntityFactory:
    @staticmethod
    def get_video_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.VIDEO,
            title='Automation Campaign '
            + datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
            sensitive_information=False,
            url='https://www.youtube.com/watch?v=nDZbgmSmJBg',
            topic='AW Admin Topic - Video',
        )
