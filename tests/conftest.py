import pytest
from src.utils.mailtrap import MailTrap


@pytest.fixture(scope="session")
def mailtrap(playwright):
    mailtrap = MailTrap(playwright)
    yield mailtrap
    mailtrap.close()
