from playwright.sync_api import Page

from src.models.auth.signup_model import EmailSignupModel
from src.page_objects.base_page import BasePage
from src.page_objects.data_types.drop_down_element import DropDown


class SignupPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.button_sign_up_with_google = page.get_by_text('Continue with Google')
        self.button_sign_up_with_microsoft = page.get_by_text('Continue with Microsoft')
        self.button_sign_up_with_email = page.get_by_text('Continue with Email')
        self.input_email = page.locator('[name="email"]')
        self.next_button = page.get_by_role('button', name='Next')
        self.input_first_name = page.get_by_role('textbox', name='First Name')
        self.input_last_name = page.get_by_role('textbox', name='Last Name')
        self.input_company_name = page.get_by_role('textbox', name='Company Name')
        self.input_password = page.get_by_role('textbox', name='Password', exact=True)
        self.input_confirm_password = page.get_by_role(
            'textbox', name='Confirm Password'
        )
        self.language_dropdown = DropDown(
            link_locator=self.page.get_by_role('combobox', name='Company Language'),
            option_list_locator=self.page.locator('[role="option"]'),
        )
        self.button_continue = page.get_by_role('button', name='Continue')
        self.go_to_login_button = page.get_by_role('link', name='Go to Log In')

    def sign_up_with_email(self, signup: EmailSignupModel):
        self.button_sign_up_with_email.click()
        self.input_email.fill(signup.email)
        self.next_button.click()
        self.input_first_name.fill(signup.first_name)
        self.input_last_name.fill(signup.last_name)
        self.input_company_name.fill(signup.company_name)
        self.input_password.fill(signup.password)
        self.input_confirm_password.fill(signup.password)
        self.language_dropdown.select_item_by_text(signup.language)
        self.button_continue.click()
        self.ensure_alert_message_is_visible('Register success')
        self.go_to_login_button.click()
