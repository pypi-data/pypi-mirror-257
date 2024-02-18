import asyncio
import atexit
import threading
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from queue import Queue
from typing import ClassVar

import aiohttp
from typing_extensions import Self

from aglog.utils import async_retry

from .time_semaphore import TimeSemaphore


@dataclass
class Request:
    method: str
    url: str
    headers: dict[str, str] | None = None
    data: dict | bytes | None = None
    json: dict | None = None
    params: list[tuple[str, str]] | dict[str, str] | None = None


@dataclass
class RequestBackendData:
    thread: threading.Thread
    queue: Queue[Request | None]


class RequestBackend:
    _singleton: ClassVar[dict[str, RequestBackendData]] = {}

    def __init__(  # noqa: PLR0913
        self: Self,
        name: str,
        stop_timeout: float = 60,
        time_calls_limit: int = 1,
        time_limit: float = 1.0,
        http_response_handler: None | Callable[[aiohttp.ClientResponse], Awaitable[None]] = None,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
        retry_exceptions: tuple[type[BaseException], ...] = (aiohttp.ClientError,),
    ) -> None:
        self.name = name
        self.stop_timeout = stop_timeout
        self.time_limit = time_limit
        self.time_calls_limit = time_calls_limit
        self.http_response_handler = http_response_handler
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.retry_exceptions = retry_exceptions

        if name in self._singleton:
            self.thread = self._singleton[name].thread
            self.queue: Queue[Request | None] = self._singleton[name].queue
        else:
            self.thread = self._start_new_thread()
            self.queue = Queue()
            self._singleton[name] = RequestBackendData(thread=self.thread, queue=self.queue)
            atexit.register(self.shutdown)

    def send(self: Self, request: Request) -> None:
        self._enqueue_request(request)

    def shutdown(self: Self) -> None:
        self._enqueue_request(None)
        self.thread.join(self.stop_timeout)
        if self.name in self._singleton:
            self._singleton.pop(self.name)

    def _start_new_thread(self: Self) -> threading.Thread:
        th = threading.Thread(target=asyncio.run, args=[self._worker()], name="RequestBackend", daemon=True)
        th.start()
        return th

    async def _worker(self: Self) -> bool:
        sem = TimeSemaphore(time_limit=self.time_limit, time_calls_limit=self.time_calls_limit)

        async with aiohttp.ClientSession() as session:
            tasks = []
            while True:
                request: Request | None = await self._dequeue_request()
                if request is None:
                    break
                send_request = self._send_request(session, request, sem)
                tasks.append(asyncio.create_task(send_request, name=f"RequestBackend [{request.method}]: {request.url}"))
                tasks = [task for task in tasks if not task.done()]
            if tasks != []:
                await asyncio.wait(tasks, timeout=self.stop_timeout)
        return True

    async def _send_request(self: Self, session: aiohttp.ClientSession, request: Request, semaphore: TimeSemaphore) -> None:
        send = HttpClient(session, self.http_response_handler).send

        @async_retry(self.retry_attempts, delay=self.retry_delay, exceptions=self.retry_exceptions)
        async def _send() -> None:
            async with semaphore:
                await send(request)

        await _send()

    def _enqueue_request(self: Self, item: Request | None) -> None:
        self.queue.put_nowait(item)

    async def _dequeue_request(self: Self) -> Request | None:
        while self.queue.empty():
            await asyncio.sleep(0.01)
        return self.queue.get_nowait()


class HttpClient:
    def __init__(
        self: Self,
        session: aiohttp.ClientSession,
        http_response_handler: Callable[[aiohttp.ClientResponse], Awaitable[None]] | None = None,
    ) -> None:
        self.session = session
        self.http_response_handler = http_response_handler

    async def send(self: Self, r: Request) -> None:
        if r.method == "GET":
            return await self._get(self.session, r)
        if r.method == "POST":
            return await self._post(self.session, r)
        msg = f"Invalid method: {r.method}"
        raise ValueError(msg)

    async def _get(self: Self, session: aiohttp.ClientSession, r: Request) -> None:
        obj = {"url": r.url, "params": r.params, "headers": r.headers}
        async with session.get(**obj) as res:
            if self.http_response_handler is not None:
                await self.http_response_handler(res)
            res.raise_for_status()

    async def _post(self: Self, session: aiohttp.ClientSession, r: Request) -> None:
        obj = {"url": str(r.url), "params": r.params, "data": r.data, "json": r.json, "headers": r.headers}
        async with session.post(**obj) as res:
            if self.http_response_handler is not None:
                await self.http_response_handler(res)
            res.raise_for_status()
