from __future__ import annotations
import sys
from typing import TypeVar
from datetime import datetime, time, timedelta, timezone, tzinfo

try:
    from zoneinfo import ZoneInfo
except ImportError:
    # ZoneInfo was introduced in Python 3.9
    ZoneInfo = None

try:
    from tzlocal import get_localzone
except ImportError:
    get_localzone = None

try:
    import pytz
except ImportError:
    pytz = None
    
T_WithTime = TypeVar('T_WithTime', datetime, time)


def parse_tz(tz: tzinfo|str = None, *, explicit_local = False):
    if tz is None or tz == 'localtime':
        if explicit_local:
            if not ZoneInfo or sys.platform == 'win32':
                # Windows does not maintain a database of timezones
                if not get_localzone:
                    raise ValueError(f"Package `tzlocal` is required (on Windows or on Python < 3.9) to retrieve local timezone.")
                return get_localzone()
            return ZoneInfo('localtime')
        else:
            return None
    elif isinstance(tz, tzinfo):
        return tz
    elif tz == 'UTC':
        return timezone.utc
    elif isinstance(tz, str):
        if not ZoneInfo or sys.platform == 'win32':
            # Windows does not maintain a database of timezones
            if not pytz:
                raise ValueError(f"Package `pytz` is required (on Windows or on Python < 3.9) to convert string to timezone.")
            return pytz.timezone(tz)
        return ZoneInfo(tz)
    else:
        raise TypeError(f"Invalid timezone type: {tz} ({type(tz).__name__})")


def is_aware(value: T_WithTime):
    # See: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    if value is None:
        return False
    return value.tzinfo is not None and value.utcoffset() is not None


def now_aware(tz: tzinfo|str = None, *, ms = True):
    """
    Get the current datetime in the timezone `tz` (use `tz=None` or `tz='localtime'` for the system local timezone).
    """
    now = datetime.now().astimezone(parse_tz(tz))
    if not ms:
        now = now.replace(microsecond=0)
    return now


def make_aware(value: T_WithTime, tz: tzinfo|str = None) -> T_WithTime:
    """
    Make a datetime aware in timezone `tz` (use `tz=None` or `tz='localtime'` for the system local timezone).
    """
    if value is None:
        return None
    if is_aware(value):
        raise ValueError("make_aware expects a naive datetime, got %s" % value)
    
    return value.replace(tzinfo=parse_tz(tz, explicit_local=True))


def is_naive(value: T_WithTime):
    return not is_aware(value)


def make_naive(value: T_WithTime, tz: tzinfo = None) -> T_WithTime:
    """
    Make a datetime naive and expressed in timezone `tz` (use `tz=None` or `tz='localtime'` for the system local timezone).
    """
    if value is None:
        return None
    if not is_aware(value):
        raise ValueError("make_naive expects an aware datetime, got %s" % value)
    
    value = value.astimezone(parse_tz(tz))
    value = value.replace(tzinfo=None)
    return value


def duration_iso_string(duration: timedelta):
    # Adapted from: django.utils.duration.duration_iso_string
    if duration < timedelta(0):
        sign = "-"
        duration *= -1
    else:
        sign = ""

    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    ms = ".{:06d}".format(microseconds) if microseconds else ""
    return "{}P{}DT{:02d}H{:02d}M{:02d}{}S".format(
        sign, days, hours, minutes, seconds, ms
    )


def _get_duration_components(duration: timedelta):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds

    minutes = seconds // 60
    seconds = seconds % 60

    hours = minutes // 60
    minutes = minutes % 60

    return days, hours, minutes, seconds, microseconds

