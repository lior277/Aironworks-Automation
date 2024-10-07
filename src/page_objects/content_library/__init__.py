from enum import Enum

attach_quiz_text = 'Attach Quiz to this content to evaluate learning even more.'
quiz_attached_text = 'Quiz Attached.'
pdf_file_attached_text = 'PDF Uploaded.'
survey_attached_text = 'Survey attached.'

content_successfully_updated_text = 'Content successfully updated.'
new_content_successfully_published_text = 'New Content successfully published.'
created_education_campaign_text = 'New Education Campaign created.'
education_content_cloned_text = 'Education content Cloned.'

sensitive_information_description_text = "Please indicate whether this content contains sensitive information. Select 'Contains' if the content includes sensitive data, which limits visibility and disables cloning. If the content does not contain sensitive information, select 'Not Contains'."


class ContentType(Enum):
    VIDEO = 'Video'
    PDF = 'PDF'
    SLIDES = 'Link'
    QUIZ = 'Quiz'
    SURVEY = 'Survey'
