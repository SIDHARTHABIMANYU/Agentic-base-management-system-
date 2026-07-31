from datetime import datetime


def is_valid_date(date_str: str) -> bool:
    """
    Expected format: YYYY-MM-DD
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_time(time_str: str) -> bool:
    """
    Expected format: HH:MM (24-hour)
    """
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


