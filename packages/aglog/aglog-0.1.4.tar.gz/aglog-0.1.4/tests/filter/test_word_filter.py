import logging

import aglog.filter.word_filter as target


def make_record(msg: str = "", name="test") -> logging.LogRecord:
    return logging.LogRecord(
        name=name,
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg=msg,
        args=(),
        exc_info=None,
        func="test",
        sinfo=None,
    )


def test_message_word_filter():
    filter = target.MessageWordFilter(includes=["foo", "bar"], excludes=["baz"])
    assert filter.filter(make_record("foo")) is True
    assert filter.filter(make_record("bar")) is True
    assert filter.filter(make_record("baz")) is False
    assert filter.filter(make_record("foobar")) is True
    assert filter.filter(make_record("bazbaz")) is False
    assert filter.filter(make_record("foobarbaz")) is False

    filter = target.MessageWordFilter(includes=["foo", "bar"], excludes=["baz"], include_type="all")
    assert filter.filter(make_record("foo")) is False
    assert filter.filter(make_record("bar")) is False
    assert filter.filter(make_record("baz")) is False
    assert filter.filter(make_record("foobar")) is True
    assert filter.filter(make_record("bazbaz")) is False
    assert filter.filter(make_record("foobarbaz")) is False

    filter = target.MessageWordFilter(includes=["foo", "bar"], excludes=[])
    assert filter.filter(make_record("foo")) is True
    assert filter.filter(make_record("bar")) is True
    assert filter.filter(make_record("baz")) is False
    assert filter.filter(make_record("foobar")) is True
    assert filter.filter(make_record("bazbaz")) is False
    assert filter.filter(make_record("foobarbaz")) is True

    filter = target.MessageWordFilter(excludes=["baz"])
    assert filter.filter(make_record("foo")) is True
    assert filter.filter(make_record("bar")) is True
    assert filter.filter(make_record("baz")) is False
    assert filter.filter(make_record("foobar")) is True
    assert filter.filter(make_record("bazbaz")) is False
    assert filter.filter(make_record("foobarbaz")) is False

    filter = target.MessageWordFilter()
    assert filter.filter(make_record("foo")) is True
    assert filter.filter(make_record("bar")) is True
    assert filter.filter(make_record("baz")) is True
    assert filter.filter(make_record("foobar")) is True
    assert filter.filter(make_record("bazbaz")) is True
    assert filter.filter(make_record("foobarbaz")) is True


def test_thread_name_filter():
    filter = target.ThreadNameFilter(includes=["MainThread"])
    assert filter.filter(make_record("foo")) is True

    filter = target.ThreadNameFilter(includes=["DummyThread"])
    assert filter.filter(make_record("foo")) is False


def test_process_name_filter():
    filter = target.ProcessNameFilter(includes=["MainProcess"])
    assert filter.filter(make_record("foo")) is True

    filter = target.ProcessNameFilter(includes=["DummyProcess"])
    assert filter.filter(make_record("foo")) is False


def test_name_filter():
    filter = target.NameFilter()
    assert filter.filter(make_record(name="test")) is True
    assert filter.filter(make_record(name="test.test")) is True

    filter = target.NameFilter(includes=["test"])
    assert filter.filter(make_record(name="test")) is True
    assert filter.filter(make_record(name="test.test")) is True
    assert filter.filter(make_record(name="test2")) is False

    filter = target.NameFilter(excludes=["test.test"])
    assert filter.filter(make_record(name="test")) is True
    assert filter.filter(make_record(name="test.test")) is False
    assert filter.filter(make_record(name="test.test.test")) is False
    assert filter.filter(make_record(name="test.test2")) is True

    filter = target.NameFilter(includes=[""])
    assert filter.filter(make_record(name="")) is True
    assert filter.filter(make_record(name="test")) is True
    assert filter.filter(make_record(name="test.test")) is True

    filter = target.NameFilter(excludes=[""])
    assert filter.filter(make_record(name="")) is False
    assert filter.filter(make_record(name="test")) is False
    assert filter.filter(make_record(name="test.test")) is False
