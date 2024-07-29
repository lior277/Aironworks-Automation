from enum import Enum

attach_quiz_text = 'Attach Quiz to this content to evaluate learning even more.'
quiz_attached_text = 'Quiz Attached'

content_successfully_updated_text = 'Content successfully updated.'
new_content_successfully_published_text = 'New Content successfully published.'
created_education_campaign_text = 'New Education Campaign created.'

sensitive_information_description_text = "Please indicate whether this content contains sensitive information. Select 'Contains' if the content includes sensitive data, which limits visibility and disables cloning. If the content does not contain sensitive information, select 'Not Contains'."


class ContentType(Enum):
    VIDEO = 'VIDEO'
    PDF = 'PDF'
    SLIDES = 'LINK'
    ASSESSMENT = 'ASSESSMENT'
