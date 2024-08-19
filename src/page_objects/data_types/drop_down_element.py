from playwright.sync_api import Locator, expect

from src.utils.log import Log


class DropDown:
    def __init__(
        self,
        link_locator: Locator,
        option_list_locator: Locator,
        extent_list_by_click_on_field: bool = True,
    ):
        self.locator = link_locator
        self.options_list = option_list_locator
        self.extent_list_by_click_on_field = extent_list_by_click_on_field

    def select_item_by_text(self, text: str, search: bool = False):
        Log.info(f'Selecting {text}')
        selected = False
        if (
            self.extent_list_by_click_on_field
            and not self.options_list.first.is_visible()
        ):
            self.locator.click()
        if search:
            self.locator.fill(text)
        option_text = []
        expect(self.options_list.first).to_be_visible(timeout=10_000)
        for option in self.options_list.all():
            option_text.append(option.text_content())
            if option.text_content() == text:
                option.click()
                selected = True
                break

        assert selected, f'Item {text} was not found in {option_text}'
