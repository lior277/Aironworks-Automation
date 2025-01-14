import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.factories.auth.user_model_factory import UserModelFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, sender_email',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'bar@aironworks.com',
            marks=allure.testcase('C31820'),
        )
    ],
)
def test_view_sender_details(
    is_emailfilter_enabled, user: UserModel, received_emails_page, sender_email: str
):
    sender = received_emails_page.get_sender(sender_email)
    sender_details_page = received_emails_page.go_to_senders_details(sender_email)
    sender_details = sender_details_page.get_sender_details()
    assert sender == sender_details, (
        f'Sender: {sender}, Sender details: {sender_details}'
    )


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            marks=allure.testcase('C31817'),
        )
    ],
)
def test_view_high_risk_email_details(
    is_emailfilter_enabled, user: UserModel, received_emails_page
):
    email = received_emails_page.get_high_risk_email()
    email_details_page = received_emails_page.go_to_high_risk_email_details()
    email_details = email_details_page.get_email_details()
    assert email == email_details, f'Email: {email}, Email details: {email_details}'


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_name',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'AironWorks',
            marks=allure.testcase('C31819'),
        )
    ],
)
def test_view_vendor_details(
    is_emailfilter_enabled, user: UserModel, vendor_name, received_emails_page
):
    vendor = received_emails_page.get_vendor(vendor_name)
    vendor_details_page = received_emails_page.go_to_vendor_details(vendor_name)
    vendor_details = vendor_details_page.get_vendor_details()
    assert vendor == vendor_details, (
        f'Vendor: {vendor}, Vendor details: {vendor_details}'
    )


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, sender_email, subject',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'bar@aironworks.com',
            'Last One I Promise',
            marks=allure.testcase('C31826'),
        )
    ],
)
def test_view_email_details_from_sender(
    is_emailfilter_enabled,
    user: UserModel,
    sender_email: str,
    subject: str,
    received_emails_page,
):
    sender_details_page = received_emails_page.open_senders_details(sender_email)
    email = sender_details_page.get_sender_email_details(subject)
    email_details_page = sender_details_page.go_to_sender_email_details()
    email_details = email_details_page.get_email_details()
    assert all(item in email_details.items() for item in email.items()), (
        f'Email: {email}, Email Details: {email_details}'
    )


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor, sender',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'AironWorks',
            'natsuki@aironworks.com',
            marks=allure.testcase('C31832'),
        )
    ],
)
def test_view_sender_details_from_vendor(
    is_emailfilter_enabled,
    user: UserModel,
    vendor: str,
    sender: str,
    received_emails_page,
):
    vendor_details_page = received_emails_page.open_vendor_details(vendor)
    sender = vendor_details_page.get_sender_details(sender)
    sender_details_page = vendor_details_page.go_to_sender_details(sender)
    sender_details = sender_details_page.get_sender_details()
    assert all(item in sender_details.items() for item in sender.items()), (
        f'Sender: {sender}, Sender details: {sender_details}'
    )


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor, email',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'AironWorks',
            '',
            marks=allure.testcase('C31833'),
        )
    ],
)
def test_view_email_details_from_vendor(
    is_emailfilter_enabled,
    user: UserModel,
    vendor: str,
    email: str,
    received_emails_page,
):
    vendor_details_page = received_emails_page.open_vendor_details(vendor)
    email = vendor_details_page.get_vendor_email_details(email)
    email_details_page = vendor_details_page.go_to_vendor_email_details()
    email_details = email_details_page.get_email_details()
    assert email is not None
    assert all(item in email_details.items() for item in email.items()), (
        f'Email: {email}, Email Details: {email_details}'
    )
