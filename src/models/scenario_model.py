from dataclasses import dataclass

from src.configs.config_loader import AppConfigs
from src.models.scenario import CampaignType


@dataclass
class ScenarioModel:
    name: str
    sender_address: str
    sender_name: str
    subject: str
    url_suffix: str
    html_content: str = '{{attack_url}}'
    sender_domain: str = AppConfigs.SENDER_DOMAIN
    link_domain: str = AppConfigs.LINKS_DOMAIN
    campaign_type: CampaignType = CampaignType.PHISHING_LINK
    file_path: str = None
