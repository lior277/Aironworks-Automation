import faker

from src.configs.config_loader import AppConfigs
from src.models.auth.login_model import LoginModel

fake = faker.Faker()


class LoginModelFactory:
    @classmethod
    def customer_admin(cls) -> LoginModel:
        return LoginModel(
            email=AppConfigs.CUSTOMER_ADMIN_USERNAME,
            password=AppConfigs.CUSTOMER_ADMIN_PASSWORD,
            remember=True,
            otp='',
            admin=False,
        )
