import allure
import pytest

from src.models.factories.auth.user_model_factory import UserModelFactory


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.parametrize(
    'user, question, question_type, keyword, number_blocks',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            'List me 3 scenarios that is email attack with "Duc" in the name',
            'search preview scenario',
            'Duc',
            3,
            marks=[allure.testcase('C31803'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'List me 3 education content that is with "Test" in the name',
            'search preview education content',
            'Test',
            3,
            marks=[allure.testcase('C31803'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'List me 3 recent simulation campaigns',
            'search preview campaign',
            '',
            3,
            marks=[allure.testcase('C31803'), pytest.mark.xdist_group(name='agent1')],
        ),
        pytest.param(
            UserModelFactory.customer_admin(),
            'List me 3 recent education campaigns',
            'search preview education campaign',
            '',
            3,
            marks=[allure.testcase('C31803'), pytest.mark.xdist_group(name='agent1')],
        ),
    ],
)
def test_ai_agent_search_preview(
    ai_agent_page, question, question_type, keyword, number_blocks
):
    ai_agent_page.ask_ai_agent(question, question_type, keyword, number_blocks)
