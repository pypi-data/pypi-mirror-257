from unittest.mock import MagicMock

import pytest

from aglog.utils import async_retry, retry


def test_retry():
    @retry()
    def func1():
        return "test"

    assert func1() == "test"

    mock = MagicMock()

    @retry(max_attempts=3, delay=0, reraise=True)
    def func2():
        mock()
        raise Exception("test")

    with pytest.raises(Exception, match="test"):
        func2()
    assert mock.call_count == 3

    @retry(max_attempts=1, delay=0, reraise=False)
    def func3():
        raise Exception("test")

    func3()

    mock = MagicMock()

    @retry(max_attempts=3, exceptions=(ValueError,), reraise=False, delay=0)
    def func4():
        mock()
        raise RuntimeError("test")

    with pytest.raises(RuntimeError, match="test"):
        func4()
    assert mock.call_count == 1


@pytest.mark.asyncio()
async def test_async_retry():
    async def func1():
        return "test"

    assert await async_retry()(func1)() == "test"

    mock = MagicMock()

    async def func2():
        mock()
        raise Exception("test")

    with pytest.raises(Exception, match="test"):
        await async_retry(max_attempts=3, delay=0, reraise=True)(func2)()
    assert mock.call_count == 3

    async def func3():
        raise Exception("test")

    await async_retry(max_attempts=1, delay=0, reraise=False)(func3)()

    mock = MagicMock()

    async def func4():
        mock()
        raise RuntimeError("test")

    with pytest.raises(RuntimeError, match="test"):
        await async_retry(max_attempts=3, exceptions=(ValueError,), reraise=False, delay=0)(func4)()
    assert mock.call_count == 1
