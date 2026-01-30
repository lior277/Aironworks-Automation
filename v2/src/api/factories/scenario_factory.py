# v2/src/api/models/scenario.py
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ScenarioKind(str, Enum):
    LINK = 'LINK'
    ATTACHMENT = 'ATTACHMENT'
    DATA_ENTRY = 'DATA_ENTRY'


class ScenarioVector(str, Enum):
    EMAIL = 'email'
    SMS = 'sms'
    VOICE = 'voice'


class ScenarioType(str, Enum):
    SIMULATION = 'SIMULATION'
    ASSESSMENT = 'ASSESSMENT'


class Language(str, Enum):
    EN = 'en'
    HE = 'he'


class SourceDetails(BaseModel):
    sender_address: str
    sender_name: str
    subject: str


class ScenarioData(BaseModel):
    """Data model for creating scenarios"""

    # Required fields
    kind: ScenarioKind
    vector: ScenarioVector
    scenario_type: ScenarioType
    language: Language
    strategy_name: str
    source_details: SourceDetails
    content: str
    tags: List[str]
    base_attack_url: str
    version: int

    # Optional fields
    data_entry_kind: Optional[str] = None
    attachment_path: Optional[str] = None
    attachment_name: Optional[str] = None
    add_insights: bool = False
    hacker_insight: Optional[str] = None
    hacker_tips: Optional[str] = None
    is_customer_generated: bool = False
    data_entry_page_id: Optional[str] = None
    is_company: bool = False
    edit_id: Optional[str] = None
    is_clone: bool = False
    edit_info: Optional[str] = None

    class Config:
        use_enum_values = True  # Auto-convert enums to values


class ScenarioResponse(BaseModel):
    """Response model from GET scenario API"""

    id: str
    kind: str
    vector: str
    scenario_type: str
    language: str
    strategy_name: str
    source_details: SourceDetails
    content: str
    tags: List[str]
    version: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # If API adds new fields, Pydantic will warn you!
