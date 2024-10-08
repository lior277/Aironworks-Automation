class CategoryEntity:
    def __init__(
        self, name: str = None, matched_statuses: list = None, message_regex: str = None
    ):
        self.name = name
        self.matchedStatuses = matched_statuses
        self.messageRegex = message_regex


class CategoryFactory:
    @classmethod
    def create_category(cls, name, matched_statuses, message_regex):
        return CategoryEntity(
            name=name, matched_statuses=matched_statuses, message_regex=message_regex
        )

    @classmethod
    def create_find_email_category(cls):
        return CategoryEntity(
            name='Unable to find email, please check it manually! -> https://mailtrap.io/inboxes',
            matched_statuses=['failed'],
            message_regex='.*Unable to find email.*',
        )
