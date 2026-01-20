"""
HTTP utilities for API automation.
"""

from urllib3.util.retry import Retry


RETRY_STATUS_CODES = [429, 500, 502, 503, 504]
RETRY_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def create_retry_strategy(
    total: int = 5,
    backoff_factor: float = 0.5,
) -> Retry:
    """
    Create retry strategy for HTTP requests.

    Retries on: 429, 500, 502, 503, 504
    Backoff: 0.5s, 1s, 2s, 4s, 8s...
    """
    return Retry(
        total=total,
        backoff_factor=backoff_factor,
        status_forcelist=RETRY_STATUS_CODES,
        allowed_methods=RETRY_METHODS,
        raise_on_status=False,
    )