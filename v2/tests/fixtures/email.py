"""Email testing fixtures."""
import random
import pytest

from v2.src.core.config import Config


@pytest.fixture(scope='session')
def mailtrap(playwright):
    """Mailtrap client for email verification."""
    from v2.src.core.utils.mailtrap import MailTrap
    mt = MailTrap(playwright)
    yield mt
    mt.close()


@pytest.fixture(scope='session')
def example_mail() -> bytes:
    """Sample email for testing."""
    with open(f'{Config.RESOURCES_PATH}/example_mail.eml', 'rb') as f:
        return f.read().replace(
            b'RANDOM_TEXT',
            str(random.randint(100000000, 999999999)).encode('utf-8')
        )