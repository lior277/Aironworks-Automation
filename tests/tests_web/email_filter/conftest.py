import pytest
from playwright.sync_api import expect

from src.apis.api_factory import api
from src.configs.config_loader import AppConfigs
from src.models.email_filter.email_domain_model import EmailDomainModel
from src.models.factories.email_filter.email_domain_model_factory import (
    EmailDomainModelFactory,
)
from src.page_objects.email_filter.sender_details_page import SenderDetailsPage
from src.page_objects.email_filter.vendor_details_page import VendorDetailsPage


@pytest.fixture(scope='function')
def add_to_block_list(
    request, api_request_context_customer_admin_email_filter
) -> EmailDomainModel:
    email_domain = EmailDomainModelFactory.get_random_email_domain_with_empty_domain()
    email_filter_service = api.email_filter(
        api_request_context_customer_admin_email_filter
    )
    expect(
        email_filter_service.block_email(email=email_domain.email_address)
    ).to_be_ok()


@pytest.fixture(scope='function')
def add_to_safe_list(
    request, api_request_context_customer_admin_email_filter
) -> EmailDomainModel:
    email_domain = EmailDomainModelFactory.get_random_email_domain_with_empty_domain()
    email_filter_service = api.email_filter(
        api_request_context_customer_admin_email_filter
    )
    expect(email_filter_service.safe_email(email=email_domain.email_address)).to_be_ok()


@pytest.fixture(scope='function')
def add_to_block_list_selected(
    request, api_request_context_customer_admin_email_filter
):
    email_domain = request.param
    email_filter_service = api.email_filter(
        api_request_context_customer_admin_email_filter
    )
    if email_domain.count('@') == 1:
        expect(email_filter_service.block_email(email_domain)).to_be_ok()
    else:
        expect(email_filter_service.block_domain(email_domain)).to_be_ok()
    return email_domain


@pytest.fixture(scope='function')
def add_to_safe_list_selected(request, api_request_context_customer_admin_email_filter):
    email_domain = request.param
    email_filter_service = api.email_filter(
        api_request_context_customer_admin_email_filter
    )
    if email_domain.count('@') == 1:
        expect(email_filter_service.safe_email(email_domain)).to_be_ok()
    else:
        expect(email_filter_service.safe_domain(email_domain)).to_be_ok()
    return email_domain


@pytest.fixture(scope='function')
def sender_details_page(request, received_emails_page) -> SenderDetailsPage:
    email = request.param
    sender_details_page = received_emails_page.open_senders_details(email)
    return sender_details_page


@pytest.fixture(scope='function')
def vendor_details_page(request, received_emails_page) -> VendorDetailsPage:
    vendor = request.param
    vendor_details_page = received_emails_page.open_vendor_details(vendor)
    return vendor_details_page


@pytest.fixture(scope='function')
def option(request, api_request_context_customer_admin_email_filter):
    email_filter_service = api.email_filter(
        api_request_context_customer_admin_email_filter
    )
    option = request.param
    if option == 'Block High-Risk Email':
        expect(email_filter_service.label_as_high_risk()).to_be_ok()
    elif option == 'Label As High-Risk Only':
        expect(email_filter_service.block_high_risk()).to_be_ok()
    else:
        raise ValueError(f'Option {option} is not supported')
    return option


@pytest.fixture(scope='function')
def remove_from_block_list(request, api_request_context_customer_admin_email_filter):
    def finalizer():
        email_filter_service = api.email_filter(
            api_request_context_customer_admin_email_filter
        )
        email_domain = getattr(request.node, 'email_domain', None)
        data = email_filter_service.list_blocked_emails_domains().json()
        email_domain_list = data.get('blocked_emails', [])
        matched = next(
            (
                item
                for item in email_domain_list
                if item.get('link') == email_domain.email_address
                or item.get('link') == email_domain.domain
            ),
            None,
        )
        id = matched.get('id')
        expect(email_filter_service.unblock_email_domain(email_id=id)).to_be_ok()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='function')
def remove_from_safe_list(request, api_request_context_customer_admin_email_filter):
    def finalizer():
        email_filter_service = api.email_filter(
            api_request_context_customer_admin_email_filter
        )
        email_domain = getattr(request.node, 'email_domain', None)
        data = email_filter_service.list_safe_emails_domains().json()
        email_domain_list = data.get('safe_emails', [])
        matched = next(
            (
                item
                for item in email_domain_list
                if item.get('link') == email_domain.email_address
                or item.get('link') == email_domain.domain
            ),
            None,
        )
        id = matched.get('id')
        expect(email_filter_service.unsafe_email_domain(email_id=id)).to_be_ok()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='function')
def remove_from_block_list_details(
    request, api_request_context_customer_admin_email_filter
):
    def finalizer():
        email_filter_service = api.email_filter(
            api_request_context_customer_admin_email_filter
        )
        email_domain = getattr(request.node, 'email_domain', None)
        data = email_filter_service.list_blocked_emails_domains().json()
        email_domain_list = data.get('blocked_emails', [])
        matched = next(
            (item for item in email_domain_list if item.get('link') == email_domain),
            None,
        )
        id = matched.get('id')
        expect(email_filter_service.unblock_email_domain(email_id=id)).to_be_ok()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='function')
def remove_from_safe_list_details(
    request, api_request_context_customer_admin_email_filter
):
    def finalizer():
        email_filter_service = api.email_filter(
            api_request_context_customer_admin_email_filter
        )
        email_domain = getattr(request.node, 'email_domain', None)
        data = email_filter_service.list_safe_emails_domains().json()
        email_domain_list = data.get('safe_emails', [])
        matched = next(
            (item for item in email_domain_list if item.get('link') == email_domain),
            None,
        )
        id = matched.get('id')
        expect(email_filter_service.unsafe_email_domain(email_id=id)).to_be_ok()

    request.addfinalizer(finalizer)


@pytest.fixture(scope='session')
def is_emailfilter_enabled():
    if AppConfigs.ENV != 'development' and AppConfigs.ENV != 'staging':
        pytest.skip('Email Filter not available')
