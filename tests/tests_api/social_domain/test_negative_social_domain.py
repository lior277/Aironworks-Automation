from typing import Generator

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
        pytest.param('www.yubicash.tokyo', marks=pytest.mark.test_id('C31669')),
        pytest.param('www.workflow.rest', marks=pytest.mark.test_id('C31670')),
        pytest.param('www.waveai.net', marks=pytest.mark.test_id('C31671')),
        pytest.param('www.utvoice.tokyo', marks=pytest.mark.test_id('C31672')),
        pytest.param('www.tax-authority.tokyo', marks=pytest.mark.test_id('C31673')),
        pytest.param('www.sprintly.shop', marks=pytest.mark.test_id('C31674')),
        pytest.param('www.softbank.rest', marks=pytest.mark.test_id('C31675')),
        pytest.param('www.snak.tokyo', marks=pytest.mark.test_id('C31676')),
        pytest.param('www.naikakufu.jp', marks=pytest.mark.test_id('C31677')),
        pytest.param('www.moondev.tokyo', marks=pytest.mark.test_id('C31678')),
        pytest.param('www.mobile-pay.jp', marks=pytest.mark.test_id('C31679')),
        pytest.param('www.minabank.net', marks=pytest.mark.test_id('C31680')),
        pytest.param('www.mail-service.tokyo', marks=pytest.mark.test_id('C31681')),
        pytest.param('www.line-info.co', marks=pytest.mark.test_id('C31682')),
        pytest.param('www.japan-gov.net', marks=pytest.mark.test_id('C31683')),
        pytest.param('www.infolist.biz', marks=pytest.mark.test_id('C31684')),
        pytest.param('www.gworkspace.site', marks=pytest.mark.test_id('C31685')),
        pytest.param('www.gonery.com', marks=pytest.mark.test_id('C31686')),
        pytest.param('www.gallup-course.biz', marks=pytest.mark.test_id('C31687')),
        pytest.param('www.cybertrain.online', marks=pytest.mark.test_id('C31688')),
        pytest.param('www.creditnow.jp', marks=pytest.mark.test_id('C31689')),
        pytest.param('www.azure-cloud.co', marks=pytest.mark.test_id('C31690')),
        pytest.param('www.aws-security.info', marks=pytest.mark.test_id('C31691')),
        pytest.param('www.aquatech.jp', marks=pytest.mark.test_id('C31692')),
        pytest.param('www.aquatec.online', marks=pytest.mark.test_id('C31693')),
        pytest.param('www.apple-support.tokyo', marks=pytest.mark.test_id('C31694')),
        pytest.param('www.daikingroup.jp', marks=pytest.mark.test_id('C31695')),
        pytest.param('www.aironworks-report.info', marks=pytest.mark.test_id('C31696')),
        pytest.param('www.security-linkedin.net', marks=pytest.mark.test_id('C31697')),
        pytest.param('www.gtm-google.site', marks=pytest.mark.test_id('C31698')),
        pytest.param('www.tvtokyo.biz', marks=pytest.mark.test_id('C31699')),
        pytest.param('www.hamagin.net', marks=pytest.mark.test_id('C31700')),
        # pytest.param('www.gitinfolab.com', marks=pytest.mark.test_id('C30815')),
    ],
)
def test_social_domain_negative(api_request_context, domain: str):
    response = api.public(api_request_context).verify_url_click(url=domain)
    expect(response).not_to_be_ok()
    assert (
        response.status == 400
        and response.text() == '{"Error":"attack url does not exist"}\n'
    )
