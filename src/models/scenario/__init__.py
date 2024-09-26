from enum import Enum


class CampaignType(Enum):
    PHISHING_LINK = 'Phishing Link'
    DATA_ENTRY_GOOGLE = 'Google'
    DATA_ENTRY_MICROSOFT = 'Microsoft'
    DATA_ENTRY_APPLE = 'Apple'
    ATTACHMENT = 'Attachment'


class ScenarioCloneMode(Enum):
    COPY_CONTENT = 1
    NEW_BODY = 2
