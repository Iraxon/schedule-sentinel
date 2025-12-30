import datetime

from .classes import Schedule, ScheduleEntry


def test_schedule() -> Schedule:
    """
    One event five seconds into the future
    """
    return [
        ScheduleEntry(
            datetime.datetime.now() + datetime.timedelta(seconds=5), f"Test event"
        )
    ]


def test_schedule2() -> Schedule:
    """
    Two events at five and
    twenty seconds
    """
    return [
        ScheduleEntry(
            datetime.datetime.now() + datetime.timedelta(seconds=5), f"Test event"
        ),
        ScheduleEntry(
            datetime.datetime.now() + datetime.timedelta(seconds=20), f"Test event"
        ),
    ]
