"""Test data fixtures."""

from uuid import uuid4

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def unique_id() -> str:
    """Unique identifier for test isolation."""
    return uuid4().hex[:8]


@pytest.fixture
def random_email(unique_id) -> str:
    """Random email for testing."""
    return f'test_{unique_id}@example.com'


@pytest.fixture
def test_employee(api_session, unique_id):
    """Create employee, cleanup after test."""
    employee = api_session.create_employee(
        email=f'emp_{unique_id}@example.com',
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
    yield employee
    api_session.delete_employee(employee['id'])


@pytest.fixture
def test_campaign(api_session, unique_id):
    """Create campaign, cleanup after test."""
    campaign = api_session.create_campaign(name=f'camp_{unique_id}')
    yield campaign
    api_session.delete_campaign(campaign['id'])
