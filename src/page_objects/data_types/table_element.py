import time
from typing import Generic, Callable, TypeVar

from playwright.sync_api import Locator

from src.utils.log import Log

T = TypeVar('T')


class Table(Generic[T]):

    def __init__(self, locator: Locator, structure: Callable[[], T]):
        self._Table__structure = structure
        self._Table__locator = locator

    def get_content(self):
        out = []
        if self._Table__locator.first.is_visible():
            elements = self._Table__locator.all()
            for element in elements:
                structure_object = self._Table__structure(element)
                out.append(structure_object)
        return out

    def get_row_by_column_value(self, column_name: str, value: str, wait_time: int = 1) -> T:
        Log.debug("Getting row by column %s with value %s from the table" % (column_name, value))
        end_time = time.time() + wait_time
        while True:
            content = self.get_content()
            for row in content:
                if getattr(row, column_name).is_visible():
                    row_value = getattr(row, column_name).text_content()
                    if row_value == value:
                        return row
            if time.time() > end_time:
                break
        return None
