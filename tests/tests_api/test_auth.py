import allure
import pytest


@allure.testcase('31126')
@pytest.mark.api
@pytest.mark.smoke
def test_login(api_request_context_customer_admin):
    pass
