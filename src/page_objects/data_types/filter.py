from time import sleep

from playwright.sync_api import Locator, expect

from src.utils.log import Log


class Filter:
    def __init__(
        self, link_locator: Locator, filter_select: Locator, filter_value: Locator
    ):
        self.button = link_locator
        self.filter_select = filter_select
        self.filter_value = filter_value

    def filter_by(self, filter_name: str, value: str, click_after: bool = True):
        Log.info(f'Filter by {filter_name} column and {value} value')
        if not self.filter_select.is_visible():
            self.button.click()
        self.filter_select.select_option(filter_name)
        self.filter_value.fill(value)
        sleep(1)  # TODO ask FE team to add some kind of spinner
        expect(self.filter_value).to_have_value(value=value)
        if click_after:
            self.button.click()
