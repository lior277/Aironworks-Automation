import os
import random
import string
from datetime import datetime

from src.configs.config_loader import AppFolders
from src.page_objects.content_library import ContentType


def get_random_title():
    return (
        f'Automation Content {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')} '
        f'{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}'
    )


class AnswerEntity:
    def __init__(self, answer: str, correct: bool = False):
        self.answer = answer
        self.correct = correct


class QuestionEntity:
    def __init__(self, question: str, quiz_score: str, answers: list[AnswerEntity]):
        self.question = question
        self.quiz_score = quiz_score
        self.answers = answers


class QuizEntity:
    def __init__(self, questions: list[QuestionEntity]):
        self.questions = questions


class ContentLibraryEntity:
    def __init__(
        self,
        content_type: ContentType,
        title: str,
        sensitive_information: bool,
        topic: str,
        url: str = None,
        pdf_file_path: str = None,
        quiz: QuizEntity = None,
    ):
        self.content_type = content_type
        self.title = title
        self.sensitive_information = sensitive_information
        self.topic = topic
        self.url = url
        self.pdf_file_path = pdf_file_path
        self.quiz = quiz


class ContentLibraryEntityFactory:
    @staticmethod
    def get_video_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.VIDEO,
            title=get_random_title(),
            sensitive_information=False,
            url='https://www.youtube.com/watch?v=nDZbgmSmJBg',
            topic='e2e Admin Topic - Video',
        )

    @staticmethod
    def get_pdf_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.PDF,
            title=get_random_title(),
            sensitive_information=False,
            pdf_file_path=os.path.join(AppFolders.RESOURCES_PATH, 'sample.pdf'),
            topic='e2e Admin Topic - PDF',
        )

    @staticmethod
    def get_slides_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.SLIDES,
            title=get_random_title(),
            sensitive_information=False,
            url='https://docs.google.com/presentation/d/1MXg2I9fVtFhFJaRwI857VN8McO5PhsNZaQnsBgY3uH0/edit?usp=sharing',
            topic='e2e Admin Topic - Slides',
        )

    @staticmethod
    def get_quiz_content() -> ContentLibraryEntity:
        return ContentLibraryEntity(
            ContentType.QUIZ,
            title=get_random_title(),
            sensitive_information=False,
            topic='e2e Admin Topic - Quiz',
            quiz=QuizEntity(
                questions=[
                    QuestionEntity(
                        'Question 1',
                        quiz_score='10',
                        answers=[
                            AnswerEntity(answer='Answer 1', correct=True),
                            AnswerEntity(answer='Answer 2'),
                        ],
                    )
                ]
            ),
        )
