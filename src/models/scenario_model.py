from dataclasses import dataclass

from src.configs.config_loader import AppConfigs


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
