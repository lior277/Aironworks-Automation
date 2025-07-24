import random
import time

import faker

from src.models.email_filter.email_domain_model import EmailDomainModel

fake = faker.Faker()


class EmailDomainModelFactory:
    @staticmethod
    def get_random_email_domain() -> EmailDomainModel:
        return EmailDomainModel(
            email_address=fake.email()
            + str(random.randint(1000, 9999))
            + str(int(time.time() * 1000))[-4:],
            domain=fake.domain_name()
            + str(random.randint(1000, 9999))
            + str(int(time.time() * 1000))[-4:],
        )

    @staticmethod
    def get_random_email_domain_with_empty_email() -> EmailDomainModel:
        return EmailDomainModel(
            email_address='',
            domain=fake.domain_name()
            + str(random.randint(1000, 9999))
            + str(int(time.time() * 1000))[-4:],
        )

    @staticmethod
    def get_random_email_domain_with_empty_domain() -> EmailDomainModel:
        return EmailDomainModel(
            email_address=fake.email()
            + str(random.randint(1000, 9999))
            + str(int(time.time() * 1000))[-4:],
            domain='',
        )
