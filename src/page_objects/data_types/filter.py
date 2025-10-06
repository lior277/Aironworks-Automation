from time import sleep

from playwright.sync_api import Locator, expect

from src.utils.log import Log


class Filter:
    def __init__(
        self,
        link_locator: Locator,
        filter_select: Locator,
        filter_value: Locator,
        loader: Locator,
        filter_options: Locator = None,
    ):
        self.button = link_locator
        self.filter_options = filter_options
        self.filter_select = filter_select
        self.filter_value = filter_value
        self.loader = loader

    def filter_by(self, filter_name: str, value: str, click_after: bool = True):
        Log.info(f'Filter by {filter_name} column and {value} value')
        if not self.filter_select.is_visible():
            self.button.click()
        sleep(3)
        # self.filter_select.select_option(filter_name)
        self.filter_select.click()
        if self.filter_options:
            self.filter_options.get_by_role(
                'option', name=filter_name, exact=True
            ).click()
        expect(self.filter_select).to_have_text(filter_name)
        self.filter_value.wait_for(state='visible')
        sleep(3)
        self.filter_value.click()
        self.filter_value.fill(value)
        self.loader.wait_for(state='hidden')
        sleep(2)  # TODO ask FE team to add some kind of spinner
        expect(self.filter_value).to_have_value(value=value)
        if click_after:
            self.button.click()
