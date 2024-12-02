import allure
import pytest

from src.models.auth.user_model import UserModel
from src.models.email_filter.email_domain_model import EmailDomainModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.email_filter.email_domain_model_factory import (
    EmailDomainModelFactory,
)


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, email_domain',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_domain(),
            marks=allure.testcase('C31803'),
        ),
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_email(),
            marks=allure.testcase('C31831'),
        ),
    ],
)
def test_add_to_block_list(
    is_emailfilter_enabled,
    email_filter_settings_page,
    user: UserModel,
    email_domain: EmailDomainModel,
    remove_from_block_list,
    request,
):
    email_filter_settings_page.add_to_block_list(email_domain)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, email_domain',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_domain(),
            marks=allure.testcase('C31822'),
        ),
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_email(),
            marks=allure.testcase('C31830'),
        ),
    ],
)
def test_add_to_safe_list(
    is_emailfilter_enabled,
    email_filter_settings_page,
    user: UserModel,
    email_domain: EmailDomainModel,
    remove_from_safe_list,
    request,
):
    email_filter_settings_page.add_to_safe_list(email_domain)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, sender_details_page, is_email',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'gitlab@mg.gitlab.com',
            True,
            marks=allure.testcase('C31821'),
        ),
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'gitlab@mg.gitlab.com',
            False,
            marks=allure.testcase('C31821'),
        ),
    ],
    indirect=['sender_details_page'],
)
def test_add_to_block_list_from_sender(
    is_emailfilter_enabled,
    request,
    user: UserModel,
    sender_details_page,
    is_email,
    remove_from_block_list_details,
):
    email_domain = sender_details_page.add_to_block_list(is_email)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, sender_details_page, is_email',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'gitlab@mg.gitlab.com',
            False,
            marks=allure.testcase('C31823'),
        ),
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'gitlab@mg.gitlab.com',
            True,
            marks=allure.testcase('C31823'),
        ),
    ],
    indirect=['sender_details_page'],
)
def test_add_to_safe_list_from_sender(
    request,
    is_emailfilter_enabled,
    user: UserModel,
    sender_details_page,
    is_email,
    remove_from_safe_list_details,
):
    email_domain = sender_details_page.add_to_safe_list(is_email)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            marks=allure.testcase('C31802'),
        )
    ],
)
def test_remove_from_block_list(
    is_emailfilter_enabled,
    email_filter_settings_page,
    user: UserModel,
    add_to_block_list,
    request,
):
    email_filter_settings_page.remove_from_block_list()


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            marks=allure.testcase('C31828'),
        )
    ],
)
def test_remove_from_safe_list(
    is_emailfilter_enabled,
    email_filter_settings_page,
    user: UserModel,
    add_to_safe_list,
    request,
):
    email_filter_settings_page.remove_from_safe_list()


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, sender',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Aironworks',
            'pham.duc@aironworks.com',
            marks=allure.testcase('C31836'),
        )
    ],
    indirect=['vendor_details_page'],
)
def test_add_sender_to_block_list_from_vendor(
    request,
    is_emailfilter_enabled,
    user: UserModel,
    vendor_details_page,
    sender,
    remove_from_block_list_details,
):
    vendor_details_page.select_sender_block(sender)
    request.node.email_domain = sender


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, domain',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Eight',
            '8card.net',
            marks=allure.testcase('C31837'),
        )
    ],
    indirect=['vendor_details_page'],
)
def test_add_domain_to_block_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    domain,
    remove_from_block_list_details,
    request,
):
    vendor_details_page.select_domain_block(domain)
    request.node.email_domain = domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, sender',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Aironworks',
            'gonen@aironworks.com',
            marks=allure.testcase('C31838'),
        )
    ],
    indirect=['vendor_details_page'],
)
def test_add_sender_to_safe_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    sender,
    remove_from_safe_list_details,
    request,
):
    vendor_details_page.select_sender_add_to_safe_list(sender)
    request.node.email_domain = sender


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, domain',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Gmail',
            'gmail.com',
            marks=allure.testcase('C31839'),
        )
    ],
    indirect=['vendor_details_page'],
)
def test_add_domain_to_safe_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    domain,
    remove_from_safe_list_details,
    request,
):
    vendor_details_page.select_domain_add_to_safe_list(domain)
    request.node.email_domain = domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, add_to_block_list_selected',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Aironworks',
            'ani@aironworks.com',
            marks=allure.testcase('C31840'),
        )
    ],
    indirect=['vendor_details_page', 'add_to_block_list_selected'],
)
def test_remove_sender_from_block_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    add_to_block_list_selected,
    request,
):
    vendor_details_page.select_sender_remove_from_block_list(add_to_block_list_selected)


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, add_to_block_list_selected',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Gitlab',
            'gitlab.com',
            marks=allure.testcase('C31841'),
        )
    ],
    indirect=['vendor_details_page', 'add_to_block_list_selected'],
)
def test_remove_domain_from_block_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    add_to_block_list_selected,
    request,
):
    vendor_details_page.select_domain_remove_from_block_list()


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, add_to_safe_list_selected',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'Aironworks',
            'taiga@aironworks.com',
            marks=allure.testcase('C31842'),
        )
    ],
    indirect=['vendor_details_page', 'add_to_safe_list_selected'],
)
def test_remove_sender_from_safe_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    add_to_safe_list_selected,
    request,
):
    vendor_details_page.select_sender_remove_from_safe_list(add_to_safe_list_selected)


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, vendor_details_page, add_to_safe_list_selected',
    [
        pytest.param(
            UserModelFactory.customer_admin_email_filter(),
            'MIND',
            'mind.co.jp',
            marks=allure.testcase('C31843'),
        )
    ],
    indirect=['vendor_details_page', 'add_to_safe_list_selected'],
)
def test_remove_domain_from_safe_list_from_vendor(
    is_emailfilter_enabled,
    vendor_details_page,
    user: UserModel,
    add_to_safe_list_selected,
    request,
):
    vendor_details_page.select_domain_remove_from_safe_list()
