# import os

# import allure
# import pytest

# from src.models.auth.user_model import UserModel
# from src.models.factories.auth.user_model_factory import UserModelFactory


# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user',
#     [
#         pytest.param(
#             UserModelFactory.user(),
#             marks=[
#                 allure.testcase('C31825'),
#                 pytest.mark.skipif(
#                     os.getenv('ENV') != 'staging', reason='Staging only'
#                 ),
#             ],
#         )
#     ],
# )
# def test_dashboard_loading(user: UserModel, employee_dashboard_page):
#     employee_dashboard_page.wait_for_page_loaded()
#     assert employee_dashboard_page.get_greeting_text() == 'Welcome, Test Test'


# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user',
#     [
#         pytest.param(
#             UserModelFactory.user(),
#             marks=[
#                 allure.testcase('C31825'),
#                 pytest.mark.skipif(
#                     os.getenv('ENV') != 'staging', reason='Staging only'
#                 ),
#             ],
#         )
#     ],
# )
# def test_previous_phishing_simulations_details(
#     user: UserModel, employee_dashboard_page
# ):
#     employee_dashboard_page.wait_for_page_loaded()
#     previous_phishing_simulations_details_page = employee_dashboard_page.go_to_details(
#         'Previous Phishing Simulations'
#     )
#     assert previous_phishing_simulations_details_page.get_first_row_data()
#     previous_phishing_simulations_details_page.click_preview_first_row()
#     assert previous_phishing_simulations_details_page.previous_phishing_simulations_preview_popup.is_visible()


# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user',
#     [
#         pytest.param(
#             UserModelFactory.user(),
#             marks=[
#                 allure.testcase('C31825'),
#                 pytest.mark.skipif(
#                     os.getenv('ENV') != 'staging', reason='Staging only'
#                 ),
#             ],
#         )
#     ],
# )
# def test_completed_education_campaigns_details(
#     user: UserModel, employee_dashboard_page
# ):
#     employee_dashboard_page.wait_for_page_loaded()
#     completed_education_campaigns_page = employee_dashboard_page.go_to_details(
#         'Completed Education Campaigns'
#     )
#     assert completed_education_campaigns_page.get_first_row_data()
#     with completed_education_campaigns_page.page.context.expect_page() as new_page_info:
#         completed_education_campaigns_page.click_first_row()
#     new_page = new_page_info.value
#     assert new_page.url.startswith(
#         'https://staging.app.aironworks.com/guest/education/'
#     )


# @pytest.mark.smoke
# @pytest.mark.web
# @pytest.mark.parametrize(
#     'user',
#     [
#         pytest.param(
#             UserModelFactory.user(),
#             marks=[
#                 allure.testcase('C31825'),
#                 pytest.mark.skipif(
#                     os.getenv('ENV') != 'staging', reason='Staging only'
#                 ),
#             ],
#         )
#     ],
# )
# def test_report_history_details(user: UserModel, employee_dashboard_page):
#     employee_dashboard_page.wait_for_page_loaded()
#     report_history_page = employee_dashboard_page.go_to_details('Report History')
#     assert report_history_page.get_first_row_data()
