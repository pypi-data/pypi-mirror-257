import logging
from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from typing_extensions import Self, override

from aglog.utils.local_timezone import get_local_timezone

TimeSpec = Literal["hours", "minutes", "seconds", "milliseconds", "microseconds"]


class Iso8601Formatter(logging.Formatter):
    def __init__(self: Self, fmt: str | None = None, datefmt: TimeSpec | None = None, timezone: str | None = None) -> None:
        local_timezone = get_local_timezone()
        self.timezone = ZoneInfo(timezone) if timezone is not None else local_timezone
        super().__init__(fmt=fmt, datefmt=datefmt)

    @override
    def formatTime(self: Self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        d = datetime.fromtimestamp(record.created, tz=self.timezone)
        return d.isoformat(timespec=datefmt or "microseconds")
