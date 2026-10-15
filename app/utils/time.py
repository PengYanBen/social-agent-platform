"""Time utilities - all times stored as UTC."""
from datetime import datetime, timezone


def utc_now():
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def to_utc(dt):
    """Convert a datetime to UTC. Naive datetimes are assumed to be UTC."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
