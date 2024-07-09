import allure
from playwright.sync_api import Page

from src.configs.config_loader import AppConfigs
from src.utils.log import Log


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.customerBaseUrl = AppConfigs.BASE_URL
        self.adminBaseUrl = AppConfigs.ADMIN_BASE_URL
        self.empty_state = self.page.get_by_test_id("empty-state")
        self.loading = self.page.get_by_text("Loading")
        self.progress_bar = self.page.get_by_role("progressbar")
        self.alert_message = self.page.locator("[id='notistack-snackbar']")
        import src.page_objects.navigation_bar

        self.navigation_bar = src.page_objects.navigation_bar.NavigationBar(page)
        self.default_url = None
        if page.url:
            self.set_default_url('/'.join(page.url.split('/', 3)[:3]) + '/')

    @allure.step("BasePage: wait for loading state")
    def wait_for_loading_state(self, timeout=10000):
        try:
            self.loading.wait_for(timeout=timeout, state="visible")
            self.loading.wait_for(timeout=timeout, state="hidden")
        except Exception as error:
            Log.info(f"{error=}")
            pass

    @allure.step("BasePage: wait for progress bar disappears")
    def wait_for_progress_bar_disappears(self, timeout=10000):
        if self.progress_bar.is_visible(timeout=timeout):
            self.progress_bar.wait_for(timeout=timeout, state="hidden")

    @allure.step("BasePage: set default {default_url} url")
    def set_default_url(self, default_url: str):
        self.default_url = default_url
