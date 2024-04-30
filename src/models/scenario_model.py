from dataclasses import dataclass


@dataclass
class ScenarioModel:
    name: str
    sender_address: str
    sender_name: str
    subject: str
    url_suffix: str
    html_content: str = "{{attack_url}}"
    sender_domain: str = "moondev.tokyo"
    link_domain: str = "staging.sd.aironworks.com"
