# import allure
# import pytest

# from src.models.auth.user_model import UserModel
# from src.models.factories.auth.user_model_factory import UserModelFactory
# from src.page_objects.education_campaign.education_campaign_modify_page import (
#     EducationCampaignModifyPage,
# )


# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user',
#     [
#         pytest.param(UserModelFactory.aw_admin(), marks=allure.testcase('31522')),
#         pytest.param(UserModelFactory.customer_admin(), marks=allure.testcase('31521')),
#     ],
# )
# def test_modify_education_campaign(
#     modify_education_campaign_page: EducationCampaignModifyPage, user: UserModel
# ):
#     modify_education_campaign_page.update_completion_date('2025-12-05')
#     modify_education_campaign_page.select_target_employees()
#     modify_education_campaign_page.add_reminder('2025-12-05 10:00')
#     modify_education_campaign_page.save_changes_button.click()
#     # expect(modify_education_campaign_page.alert_message).to_have_text(modify_campaign_successfully_text)
