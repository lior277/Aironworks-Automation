import re

RE_URL = re.compile(
    r'(?<! src=\")'
    r'(?:ftp|https?):\/\/[\w_-]+(?:\.[\w_-]+)+[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]'
)

TEXT_CONTENT_TYPES = {'text/plain', 'text/html'}


def get_text_links(text: str) -> set[str]:
    return list(set(RE_URL.findall(text)))


def attack_url_to_api_url_input(url: str) -> str:
    return url.removeprefix('https://')
