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
            UserModelFactory.customer_admin(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_domain(),
            marks=allure.testcase('C31803'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_email(),
            marks=allure.testcase('C31804'),
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
            UserModelFactory.customer_admin(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_domain(),
            marks=allure.testcase('C31822'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            EmailDomainModelFactory.get_random_email_domain_with_empty_email(),
            marks=allure.testcase('C31822'),
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
            UserModelFactory.customer_admin(),
            'gitlab@mg.gitlab.com',
            True,
            marks=allure.testcase('C31822'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'gitlab@mg.gitlab.com',
            False,
            marks=allure.testcase('C31822'),
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
    remove_from_block_list_sender,
):
    email_domain = sender_details_page.add_to_block_list(is_email)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, sender_details_page, is_email',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'gitlab@mg.gitlab.com',
            False,
            marks=allure.testcase('C31822'),
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'gitlab@mg.gitlab.com',
            True,
            marks=allure.testcase('C31822'),
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
    remove_from_safe_list_sender,
):
    email_domain = sender_details_page.add_to_safe_list(is_email)
    request.node.email_domain = email_domain


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user',
    [pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('C31803'))],
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
    [pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('C31804'))],
)
def test_remove_from_safe_list(
    is_emailfilter_enabled,
    email_filter_settings_page,
    user: UserModel,
    add_to_safe_list,
    request,
):
    email_filter_settings_page.remove_from_safe_list()
