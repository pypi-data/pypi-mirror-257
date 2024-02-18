import asyncio
import time

import pytest

import aglog.utils.time_semaphore as target


class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()

    def __call__(self):
        return time.perf_counter() - self.start_time


@pytest.mark.asyncio()
async def test_time_semaphore():
    async def inner(num: int, wait_time: float = 0.001):
        await asyncio.sleep(wait_time)
        return num

    async def outer(num: int, sem, wait_time: float = 0.001):
        async with sem:
            return await inner(num, wait_time)

    sem = target.TimeSemaphore(entire_calls_limit=1)
    tasks = [asyncio.create_task(outer(i, sem)) for i in range(3)]
    timer = Timer()
    await asyncio.wait(tasks)
    assert timer() > 0.003
    tasks = [asyncio.create_task(sem(inner)(i)) for i in range(3)]
    timer = Timer()
    await asyncio.wait(tasks)
    assert timer() > 0.003

    sem = target.TimeSemaphore(entire_calls_limit=None, time_limit=0.001, time_calls_limit=1)
    tasks = [asyncio.create_task(outer(i, sem)) for i in range(3)]
    timer = Timer()
    await asyncio.wait(tasks)
    assert timer() > 0.003

    # キャンセル
    sem = target.TimeSemaphore(time_calls_limit=1, time_limit=2)

    async def cancel():
        with pytest.raises(asyncio.CancelledError):
            async with sem:
                await asyncio.sleep(100)

    task1 = asyncio.create_task(cancel())  # sem._value -> 0
    await asyncio.sleep(0)
    assert sem._value == 0
    task2 = asyncio.create_task(cancel())  # sem._valueに変化なし
    await asyncio.sleep(0)
    assert sem._value == 0
    sem._wake_up_next()  # sem._value -> 1
    assert sem._value == 1
    task2.cancel()
    assert sem._value == 1
    task1.cancel()
