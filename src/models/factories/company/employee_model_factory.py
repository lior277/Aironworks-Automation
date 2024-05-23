import random
import string

import faker

from src.models.company.employee_model import EmployeeModel
from tests.conftest import print_execution_time

fake = faker.Faker()


class EmployeeModelFactory:
    @staticmethod
    def get_random_employee(email: str = None) -> EmployeeModel:
        return EmployeeModel(first_name=fake.first_name(), last_name=fake.last_name(),
                             email=email if email else fake.email())

    @staticmethod
    @print_execution_time
    def get_random_employees(count: int, email_name: str = None, domain: str = None) -> list[EmployeeModel]:
        emails = EmployeeModelFactory.get_random_emails(count, email_name, domain)
        return [EmployeeModelFactory.get_random_employee(email) for email in emails]

    @staticmethod
    def get_random_emails(count: int, email_name: str = None, domain: str = None) -> list[str]:
        emails = set()
        while len(emails) < count:
            unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            email = f"{f"{email_name}+" if email_name else fake.first_name()}{unique_id}@{domain if domain else fake.domain_name()}"
            emails.add(email)
        return list(emails)
