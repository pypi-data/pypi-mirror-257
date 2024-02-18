import logging

import aiohttp
from typing_extensions import Self, override

from aglog.utils.request_backend import Request, RequestBackend


class HTTPHandler(logging.Handler):
    retry_exceptions: tuple[type[BaseException], ...] = (aiohttp.ClientError,)
    retry_attempts: int = 3
    retry_delay: float = 1.0

    def __init__(
        self: Self,
        stop_timeout: float = 60.0,
        rate_limit: int = 1,
        formatter: logging.Formatter | None = None,
        level: int = logging.NOTSET,
    ) -> None:
        self.request_backend = RequestBackend(
            name=self.__class__.__name__,
            stop_timeout=stop_timeout,
            time_calls_limit=rate_limit,
            http_response_handler=self.http_response_handler,
            retry_attempts=self.retry_attempts,
            retry_delay=self.retry_delay,
            retry_exceptions=self.retry_exceptions,
        )
        super().__init__(level)
        super().setFormatter(formatter)

    @override
    def close(self: Self) -> None:
        self.request_backend.shutdown()
        super().close()

    @override
    def emit(self: Self, record: logging.LogRecord) -> None:
        request = self.get_request(record)
        self.request_backend.send(request)

    def get_request(self: Self, record: logging.LogRecord) -> Request:
        raise NotImplementedError  # pragma: no cover

    async def http_response_handler(self: Self, response: aiohttp.ClientResponse) -> None:
        pass  # pragma: no cover
