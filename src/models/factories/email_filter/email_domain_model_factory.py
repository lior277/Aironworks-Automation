import faker

from src.models.email_filter.email_domain_model import EmailDomainModel

fake = faker.Faker()


class EmailDomainModelFactory:
    @staticmethod
    def get_random_email_domain() -> EmailDomainModel:
        return EmailDomainModel(email_address=fake.email(), domain=fake.domain_name())

    @staticmethod
    def get_random_email_domain_with_empty_email() -> EmailDomainModel:
        return EmailDomainModel(email_address='', domain=fake.domain_name())

    @staticmethod
    def get_random_email_domain_with_empty_domain() -> EmailDomainModel:
        return EmailDomainModel(email_address=fake.email(), domain='')
