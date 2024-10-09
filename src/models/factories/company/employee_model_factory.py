import random
import string

import faker

from src.configs.config_loader import AppConfigs
from src.models.company.employee_model import EmployeeModel

fake = faker.Faker()


class EmployeeModelFactory:
    @staticmethod
    def get_random_employee(email: str = None) -> EmployeeModel:
        return EmployeeModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email if email else fake.email(),
            language=random.choice(['English', 'Japanese', 'Chinese']),
        )

    @staticmethod
    def get_random_employee_with_accessible_email() -> EmployeeModel:
        return EmployeeModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=AppConfigs.EMPLOYEE_INBOX % fake.pystr().lower(),
            language=random.choice(['English', 'Japanese', 'Chinese']),
        )

    @staticmethod
    def get_random_employees(
        count: int,
        email_name: str = None,
        domain: str = None,
        mailtrap_inbox: str = None,
    ) -> list[EmployeeModel]:
        emails = EmployeeModelFactory.get_random_emails(
            count, email_name, domain, mailtrap_inbox=mailtrap_inbox
        )
        return [EmployeeModelFactory.get_random_employee(email) for email in emails]

    @staticmethod
    def get_random_emails(
        count: int,
        email_name: str = None,
        domain: str = None,
        mailtrap_inbox: str = None,
    ) -> list[str]:
        emails = set()
        while len(emails) < count:
            if mailtrap_inbox:
                email = mailtrap_inbox % fake.pystr().lower()
            else:
                unique_id = ''.join(
                    random.choices(string.ascii_lowercase + string.digits, k=8)
                )
                email = f"{f"{email_name}+" if email_name else fake.first_name()}{unique_id}@{domain if domain else fake.domain_name()}"
            emails.add(email)
        return list(emails)
