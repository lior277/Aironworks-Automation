import pytest

from src.models.auth.user_model import UserModel
from src.models.automatic_campaign_model import AutomaticCampaignModel
from src.models.factories.auth.user_model_factory import UserModelFactory
from src.models.factories.operation.automatic_campaign_model_factory import (
    AutomaticCampaignModelFactory,
)
from src.page_objects.operations.operations_list_page import OperationsListPage


@pytest.mark.parametrize(
    'user, automatic_campaign',
    [
        pytest.param(
            UserModelFactory.customer_admin(),
            AutomaticCampaignModelFactory.get_automatic_campaign(),
        )
    ],
)
def test_create_automatic_campaign(
    user: UserModel,
    automatic_campaign: AutomaticCampaignModel,
    operations_list_page: OperationsListPage,
):
    create_automatic_campaign_page = (
        operations_list_page.navigate_to_create_automatic_campaign_page()
    )
    create_automatic_campaign_page.create_automatic_campaign(automatic_campaign)
