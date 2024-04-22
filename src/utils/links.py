import re

RE_URL = re.compile(
    r"(?<! src=\")"
    r"(?:ftp|https?):\/\/[\w_-]+(?:\.[\w_-]+)+[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]"
)

TEXT_CONTENT_TYPES = {"text/plain", "text/html"}


def get_text_links(text: str) -> set[str]:
    return set(RE_URL.findall(text))
