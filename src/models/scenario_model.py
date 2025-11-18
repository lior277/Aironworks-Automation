from dataclasses import dataclass

from src.configs.config_loader import AppConfigs
from src.models.scenario import CampaignType, TargetDetails


@dataclass
class ScenarioModel:
    name: str
    vector: str
    sender_address: str
    sender_name: str
    subject: str
    url_suffix: str
    html_content: str = '{{attack_url}}'
    sender_domain: str = AppConfigs.SENDER_DOMAIN
    link_domain: str = AppConfigs.LINKS_DOMAIN
    campaign_type: CampaignType = CampaignType.PHISHING_LINK
    custom_text: str = None
    custom_text_web_sms: str = None
    target_details: TargetDetails = None
    file_path: str = None
