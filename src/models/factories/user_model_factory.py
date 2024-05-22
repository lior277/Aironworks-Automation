import faker
import random
import string
from src.models.user_model import UserModel
from src.configs.config_loader import AppConfigs

fake = faker.Faker()


class UserModelFactory:
    @staticmethod
    def user():
        return UserModel(
            email="".join(random.choices(string.ascii_lowercase + string.digits, k=8))
            + "@"
            + fake.domain_name(),
            password=fake.password(),
            company=fake.company(),
            is_admin=False,
        )

    @staticmethod
    def customer_admin():
        return UserModel(
            email=AppConfigs.CUSTOMER_ADMIN_USERNAME,
            password=AppConfigs.CUSTOMER_ADMIN_PASSWORD,
            company=AppConfigs.QA_COMPANY_NAME,
            is_admin=False,
        )

    @staticmethod
    def aw_admin():
        return UserModel(
            email=AppConfigs.AW_ADMIN_USERNAME,
            password=AppConfigs.AW_ADMIN_PASSWORD,
            is_admin=True,
        )

    @staticmethod
    def reseller_admin():
        return UserModel(
            email=AppConfigs.RESELLER_ADMIN_USERNAME,
            password=AppConfigs.RESELLER_ADMIN_PASSWORD,
            is_admin=True,
            is_reseller=True,
        )
