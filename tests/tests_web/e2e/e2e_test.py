import allure
import pytest

from src.configs.config_loader import AppConfigs
from src.models.auth.signup_model import EmailSignupModel
from src.models.auth.user_model import UserModel
from src.models.factories.auth.signup_model_factory import SignupModelFactory
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.page_objects.login_page import SignInPage
from src.utils.randomizer import generate_string


@pytest.mark.parametrize(
    'user, company',
    [
        pytest.param(
            UserModelFactory.aw_admin(),
            SignupModelFactory.random_customer_ui(),
            id='customer_admin_company1',
        )
    ],
)
@pytest.mark.smoke
@allure.testcase('31554')
def test_new_user_create_group(
    user,
    company: EmailSignupModel,
    sign_in_page: SignInPage,
    request: pytest.FixtureRequest,
):
    if AppConfigs.ENV != 'staging':
        pytest.skip('This test is only for staging environment')
    sign_in_page.navigate()
    signup_page = sign_in_page.navigate_to_sign_up_page()
    signup_page.sign_up_with_email(company)
    new_user = UserModel(
        email=company.email,
        password=company.password,
        is_admin=False,
        company=company.company_name,
    )
    sign_in_page.navigate(admin=True)
    dashboard_page = sign_in_page.fill_sign_in_form(user)
    customers_page = dashboard_page.navigation_bar.navigate_customers_page()
    customers_page.navigate_to_new_customers_page()
    customers_page.approve_customer(new_user.company)
    customers_page.navigation_bar.log_out()
    sign_in_page.navigate(admin=False)
    dashboard_page = sign_in_page.fill_sign_in_form(new_user)
    groups_page = dashboard_page.navigation_bar.navigate_groups_page()
    groups_page.create_group(generate_string())


@pytest.mark.parametrize(
    'user', [pytest.param(UserModelFactory.customer_admin(), id='123')]
)
@pytest.mark.smoke
@allure.testcase('31554')
def test_new_user_create_multi_content_campaign(user, education_campaign_page):
    create_campaign_page = education_campaign_page.open_create_campaign_page()
    create_campaign_page.set_campaign_name('Test Campaign')
    select_content_page = create_campaign_page.select_content()
    select_content_page.set_name_filter('Multiple Quiz')
    select_content_page.select_content('Multiple Quiz')
    select_content_page.set_name_filter('Multiple Survey')
    select_content_page.select_content('Multiple Survey')
    select_content_page.complete_selection()
    create_campaign_page.create_campaign()
