from datetime import datetime


def utc_unix_time_datetime(nix_time: int) -> datetime:
    """
    Takes utc nix time in seconds or nanoseconds and returns date as Datetime.

    :param nix_time: Nix time to convert to string date.
    :return: Converted date as string.
    """
    try:
        date = datetime.utcfromtimestamp(nix_time)
    except OSError:  # Case when unix time is in nanoseconds
        date = datetime.utcfromtimestamp(nix_time / 1000000000)
    return date
