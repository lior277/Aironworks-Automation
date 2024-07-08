from datetime import datetime


def timestamp_to_time(timestamp: float, datetime_format: str = '%-m/%-d/%Y %-I:%M %p', lower: bool = True) -> str:
    result = datetime.fromtimestamp(timestamp).strftime(datetime_format)
    if lower:
        return result.lower()
    return result
