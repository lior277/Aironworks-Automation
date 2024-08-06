import random
import string

import faker

from src.configs.config_loader import AppConfigs
from src.models.auth.user_model import UserModel

fake = faker.Faker()


class UserModelFactory:
    @staticmethod
    def user() -> UserModel:
        return UserModel(
            email=''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            + '@'
            + fake.domain_name(),
            password=fake.password(),
            company=fake.company(),
            is_admin=False,
        )

    @staticmethod
    def customer_admin() -> UserModel:
        return UserModel(
            email=AppConfigs.CUSTOMER_ADMIN_USERNAME,
            password=AppConfigs.CUSTOMER_ADMIN_PASSWORD,
            company=AppConfigs.QA_COMPANY_NAME,
            is_admin=False,
        )

    @staticmethod
    def aw_admin() -> UserModel:
        return UserModel(
            email=AppConfigs.AW_ADMIN_USERNAME,
            password=AppConfigs.AW_ADMIN_PASSWORD,
            is_admin=True,
        )

    @staticmethod
    def reseller_admin() -> UserModel:
        return UserModel(
            email=AppConfigs.RESELLER_ADMIN_USERNAME,
            password=AppConfigs.RESELLER_ADMIN_PASSWORD,
            is_admin=True,
            is_reseller=True,
        )

    @staticmethod
    def customer_admin_upload() -> UserModel:
        return UserModel(
            email=AppConfigs.CUSTOMER_ADMIN_UPLOAD_USERNAME,
            password=AppConfigs.CUSTOMER_ADMIN_UPLOAD_PASSWORD,
            company='Upload Admin',
            is_admin=False,
        )
