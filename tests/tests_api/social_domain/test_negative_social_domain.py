from typing import Generator

import allure
import pytest
from playwright.sync_api import APIRequestContext, Playwright, expect

from src.apis.api_factory import api


@pytest.fixture(scope='function')
def api_request_context(
    playwright: Playwright, domain
) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(base_url=f'https://{domain}')
    yield request_context
    request_context.dispose()


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize(
    'domain',
    [
        pytest.param('www.yubicash.tokyo', marks=allure.testcase('31669')),
        pytest.param('www.workflow.rest', marks=allure.testcase('31670')),
        pytest.param('www.waveai.net', marks=allure.testcase('31671')),
        pytest.param('www.utvoice.tokyo', marks=allure.testcase('31672')),
        pytest.param('www.tax-authority.tokyo', marks=allure.testcase('31673')),
        pytest.param('www.sprintly.shop', marks=allure.testcase('31674')),
        pytest.param('www.softbank.rest', marks=allure.testcase('31675')),
        pytest.param('www.snak.tokyo', marks=allure.testcase('31676')),
        pytest.param('www.naikakufu.jp', marks=allure.testcase('31677')),
        pytest.param('www.moondev.tokyo', marks=allure.testcase('31678')),
        pytest.param('www.mobile-pay.jp', marks=allure.testcase('31679')),
        pytest.param('www.minabank.net', marks=allure.testcase('31680')),
        pytest.param('www.mail-service.tokyo', marks=allure.testcase('31681')),
        pytest.param('www.line-info.co', marks=allure.testcase('31682')),
        pytest.param('www.japan-gov.net', marks=allure.testcase('31683')),
        pytest.param('www.infolist.biz', marks=allure.testcase('31684')),
        pytest.param('www.gworkspace.site', marks=allure.testcase('31685')),
        pytest.param('www.gonery.com', marks=allure.testcase('31686')),
        pytest.param('www.gallup-course.biz', marks=allure.testcase('31687')),
        pytest.param('www.cybertrain.online', marks=allure.testcase('31688')),
        pytest.param('www.creditnow.jp', marks=allure.testcase('31689')),
        pytest.param('www.azure-cloud.co', marks=allure.testcase('31690')),
        pytest.param('www.aws-security.info', marks=allure.testcase('31691')),
        pytest.param('www.aquatech.jp', marks=allure.testcase('31692')),
        pytest.param('www.aquatec.online', marks=allure.testcase('31693')),
        pytest.param('www.apple-support.tokyo', marks=allure.testcase('31694')),
        pytest.param('www.daikingroup.jp', marks=allure.testcase('31695')),
        pytest.param('www.aironworks-report.info', marks=allure.testcase('31696')),
        pytest.param('www.security-linkedin.net', marks=allure.testcase('31697')),
        pytest.param('www.gtm-google.site', marks=allure.testcase('31698')),
        pytest.param('www.tvtokyo.biz', marks=allure.testcase('31699')),
        pytest.param('www.hamagin.net', marks=allure.testcase('31700')),
        # pytest.param('www.gitinfolab.com', marks=allure.testcase('30815')),
        pytest.param('www.windwyse.com', marks=allure.testcase('31702')),
        pytest.param('www.techify.biz', marks=allure.testcase('31703')),
        pytest.param('www.cyblogg.com', marks=allure.testcase('31704')),
        pytest.param('www.schedulespal.com', marks=allure.testcase('31705')),
        pytest.param('www.techcrunchweb.com', marks=allure.testcase('31706')),
        pytest.param('www.snaky.live', marks=allure.testcase('31707')),
        pytest.param('www.expresstoday.net', marks=allure.testcase('31708')),
        pytest.param('www.gmailsecurity.net', marks=allure.testcase('31709')),
        pytest.param('www.gov-info.org', marks=allure.testcase('31710')),
    ],
)
def test_social_domain_negative(api_request_context, domain: str):
    response = api.public(api_request_context).verify_url_click(url=domain)
    expect(response).not_to_be_ok()
    assert (
        response.status == 400
        and response.text() == '{"Error":"attack url does not exist"}\n'
    )
