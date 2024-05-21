import datetime
import time
from typing import Callable
from playwright.sync_api import Response


def wait_for(predicate, timeout):
    start_time = datetime.datetime.now()
    while True:
        if predicate():
            return True
        if (datetime.datetime.now() - start_time).seconds > timeout:
            return False
        time.sleep(1)


def wait_for_lro(
    lro_request: Callable[[], Response], timeout, end_status=("DONE", "ERROR")
):
    def _wait_for():
        result = lro_request()
        if result.status != 200:
            return False
        return result.json()["status"] in end_status

    wait_for(_wait_for, timeout)

    return lro_request()
