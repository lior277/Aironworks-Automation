from dataclasses import dataclass
from enum import Enum

from src.configs.config_loader import AppConfigs


class CampaignType(Enum):
    PHISHING_LINK = 'Phishing Link'
    DATA_ENTRY_GOOGLE = 'Google'
    DATA_ENTRY_MICROSOFT = 'Microsoft'
    DATA_ENTRY_APPLE = 'Apple'
    ATTACHMENT = 'Attachment'


class ScenarioCloneMode(Enum):
    COPY_CONTENT = 1
    NEW_BODY = 2


class TargetType(Enum):
    EMPLOYEE = 'Employee Attack'
    COMPANY = 'Company Attack'


@dataclass
class TargetDetails:
    target_type: TargetType
    target_company: str = None
