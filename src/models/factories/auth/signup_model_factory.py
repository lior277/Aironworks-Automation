import faker

from src.models.auth.signup_model import EmailSignupModel

fake = faker.Faker()


class SignupModelFactory:
    @classmethod
    def random_customer(cls, referral=None):
        return EmailSignupModel(
            email=fake.email(),
            password=fake.password(),
            language='en',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            company_name=fake.name(),
            referral=referral,
        )
