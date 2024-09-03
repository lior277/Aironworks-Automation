import random
import string

import faker

fake = faker.Faker()


def get_random_email() -> str:
    return (
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        + '@'
        + fake.domain_name()
    )


def generate_string(length: int = 8) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))
