# import allure
# import pytest
#
# from src.models.auth.user_model import UserModel
# from src.models.factories.auth.user_model_factory import UserModelFactory
# from src.page_objects.const import id_number_copied_text
# from src.page_objects.dashboard_page import DashboardPage
#
#
# @pytest.mark.parametrize(
#     'user, feedback',
#     [
#         pytest.param(
#             UserModelFactory.customer_admin(),
#             'Test feedback',
#             marks=allure.testcase('31667'),
#         )
#     ],
# )
# @allure.testcase('31667')
# @pytest.mark.smoke
# def test_support_menu(user: UserModel, dashboard_page: DashboardPage, feedback):
#     dashboard_page.support_menu.open_feedback_form()
#     dashboard_page.support_menu.submit_feedback_form(feedback)
#     dashboard_page.ensure_alert_message_is_visible(id_number_copied_text)
