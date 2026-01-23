import logging
import time
from functools import wraps
from typing import Tuple, Type

LOGGER = logging.getLogger(__name__)


def retry(
    times: int = 2,
    delay: float = 0.5,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
):
    """Simple retry decorator."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 2):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    LOGGER.warning(f'Retry {attempt}/{times + 1} failed: {exc}')
                    if attempt > times:
                        break
                    time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator
