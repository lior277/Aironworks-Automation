import faker

from src.models.auth.signup_model import EmailSignupModel
from src.utils.randomizer import get_random_email

fake = faker.Faker()


class SignupModelFactory:
    @classmethod
    def random_customer(cls, referral=None):
        return EmailSignupModel(
            email=get_random_email(),
            password=fake.password(),
            language='en',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            company_name=fake.name(),
            referral=referral,
        )

    @classmethod
    def random_customer_ui(cls, referral=None):
        return EmailSignupModel(
            email=get_random_email(),
            password=fake.password(special_chars=True),
            language='English',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            company_name=fake.name(),
            referral=referral,
        )
