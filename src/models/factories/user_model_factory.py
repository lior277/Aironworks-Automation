import faker

from src.models.user_model import UserModel

fake = faker.Faker()


class UserModelFactory:

    @staticmethod
    def user():
        return UserModel(email=fake.email(), password=fake.password(), company=fake.company())

    @staticmethod
    def my_user():
        return UserModel(email="test_user@gmail.com", password="Password123!@#", company="TestCompany")
