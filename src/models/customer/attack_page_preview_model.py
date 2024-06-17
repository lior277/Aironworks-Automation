from dataclasses import dataclass
from typing import Optional

from src.models.base_dataclass import BaseDataClass


@dataclass
class AttackPagePreviewModel(BaseDataClass):
    light_mode: Optional[bool]
    show_survey_button: Optional[bool]
    custom_sd_body: Optional[str] = None
    custom_sd_logo_url: Optional[str] = None
    custom_sd_warning: Optional[str] = None
