import time
from typing import Callable, Generic, TypeVar

from playwright.sync_api import Locator

from src.utils.log import Log

T = TypeVar('T')


class Table(Generic[T]):
    def __init__(
        self,
        locator: Locator,
        structure: Callable[[Locator], T],
        utility: Locator = None,
    ):
        self._Table__structure = structure
        self._Table__locator = locator
        self.loading = self._Table__locator.get_by_text('Loading')
        self.utility = utility

    def get_content(self) -> list[T]:
        out = []
        if self._Table__locator.first.is_visible():
            self._Table__locator.first.scroll_into_view_if_needed()
            elements = self._Table__locator.all()
            for element in elements:
                structure_object = self._Table__structure(element)
                out.append(structure_object)
        return out

    def get_row_count(self) -> int:
        return len(self._Table__locator.all())

    def text_content(self) -> list[list[str]]:
        all_context = []
        for element in self.get_content():
            out = []
            for i in range(20):
                self._Table__locator.page.keyboard.press('ArrowLeft')
            for fild in vars(element).values():
                count = 0
                while not fild.is_visible() and count < 20:
                    self._Table__locator.page.keyboard.press('ArrowRight')
                    count += 1
                fild.scroll_into_view_if_needed()
                out.append(fild.text_content(timeout=0))
                fild.click()
            all_context.append(out)
        return all_context

    def get_row_by_column_value(self, column_name: str, value: str) -> T:
        Log.debug(
            'Getting row by column %s with value %s from the table'
            % (column_name, value)
        )
        return self._Table__structure(
            self._Table__locator.filter(
                has=getattr(
                    self._Table__structure(self._Table__locator.page), column_name
                ).get_by_text(value)
            )
        )

    def get_row_by_index(self, index: int) -> T:
        Log.debug('Getting row by index %s from the table' % index)
        return self._Table__structure(self._Table__locator.nth(index))

    def get_last_row(self) -> T:
        Log.debug('Getting last row from the table')
        return self._Table__structure(self._Table__locator.last)

    def wait_for_loading(self, timeout=10000):
        if self.loading.first.is_visible(timeout=timeout):
            for load in self.loading.all():
                if load.is_visible():
                    load.wait_for(timeout=timeout, state='hidden')
        time.sleep(2)

    def go_to_next_page(self):
        if self.utility:
            self.utility.get_by_role('button', name='Go to next page').click()

    def go_to_previous_page(self):
        if self.utility:
            self.utility.get_by_role('button', name='Go to previous page').click()

    def get_page_count(self):
        if self.utility:
            return self.utility.locator(
                '.MuiTablePagination-displayedRows'
            ).text_content()
