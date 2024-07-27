import time
from typing import Generic, Callable, TypeVar

from playwright.sync_api import Locator

from src.utils.log import Log

T = TypeVar('T')


class Table(Generic[T]):
    def __init__(self, locator: Locator, structure: Callable[[Locator], T]):
        self._Table__structure = structure
        self._Table__locator = locator

    def get_content(self) -> list[T]:
        out = []
        if self._Table__locator.first.is_visible():
            self._Table__locator.first.scroll_into_view_if_needed()
            elements = self._Table__locator.all()
            for element in elements:
                structure_object = self._Table__structure(element)
                out.append(structure_object)
        return out

    def text_content(self) -> list[list[str]]:
        all_context = []
        for element in self.get_content():
            out = []
            for fild in vars(element).values():
                fild.scroll_into_view_if_needed()
                out.append(fild.text_content())
            all_context.append(out)
        return all_context

    def get_row_by_column_value(
        self, column_name: str, value: str, wait_time: int = 1
    ) -> T:
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
