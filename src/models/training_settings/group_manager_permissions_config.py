from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class GroupManagerPermissionsConfig(BaseDataClass):
    edit_employees_feature: Optional[bool] = None
    launch_campaigns_feature: Optional[bool] = None
    read_campaigns_data_feature: Optional[bool] = None
    resend_emails_feature: Optional[bool] = None
    read_gamification_data_feature: Optional[bool] = None
