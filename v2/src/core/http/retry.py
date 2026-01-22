import time
from typing import Callable

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class RetryPolicy:
    def __init__(
        self,
        retries: int = 2,
        delay: float = 1.0,
        retry_on_status: tuple[int, ...] = (500, 502, 503, 504),
    ):
        self.retries = retries
        self.delay = delay
        self.retry_on_status = retry_on_status

    def run(self, func: Callable):
        last_exc = None

        for attempt in range(self.retries + 1):
            try:
                response = func()

                # retry on 5xx
                if (
                    hasattr(response, 'status')
                    and response.status in self.retry_on_status
                ):
                    raise RuntimeError(f'Retryable status {response.status}')

                return response

            except (PlaywrightTimeoutError, PlaywrightError, RuntimeError) as e:
                last_exc = e
                if attempt >= self.retries:
                    break
                time.sleep(self.delay)

        raise last_exc
