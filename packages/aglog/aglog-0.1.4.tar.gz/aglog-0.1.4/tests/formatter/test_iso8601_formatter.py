import logging

import freezegun

import aglog.formatter.iso8601_formatter as target


@freezegun.freeze_time("1970-01-01 00:00:00")
def test_iso8601_formatter():
    formatter = target.Iso8601Formatter(fmt="%(asctime)s %(levelname)s %(message)s", timezone="UTC")

    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test",
        args=(),
        exc_info=None,
        func="test_func",
    )

    assert formatter.format(record) == "1970-01-01T00:00:00.000000+00:00 INFO test"
