import asyncio
import logging
import time
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import ParamSpec, TypeVar

R = TypeVar("R")
P = ParamSpec("P")


logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    *,
    delay: float = 1,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    reraise: bool = False,
) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:  # noqa: PERF203
                    attempts += 1
                    logger.debug(
                        "Retry %s/%s after exception: %s",
                        attempts,
                        max_attempts,
                        e,
                        exc_info=True,
                        extra={"exceptions": exceptions, "delay": delay},
                    )
                    if attempts >= max_attempts:
                        if reraise:
                            raise
                        break
                    time.sleep(delay)
            logger.warning("Retry limit exceeded", exc_info=True)
            return None

        return wrapper

    return decorator


def async_retry(
    max_attempts: int = 3,
    *,
    delay: float = 1,
    exceptions: tuple[type[BaseException], ...] = (Exception,),
    reraise: bool = False,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R | None]]]:
    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R | None]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            attempts = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:  # noqa: PERF203
                    attempts += 1
                    logger.debug(
                        "Retry %s/%s after [%s]: %s",
                        attempts,
                        max_attempts,
                        type(e),
                        e,
                        exc_info=True,
                        extra={"exceptions": exceptions, "delay": delay},
                    )
                    if attempts >= max_attempts:
                        if reraise:
                            raise
                        break
                    await asyncio.sleep(delay)
            logger.warning("Retry limit exceeded", exc_info=True)
            return None

        return wrapper

    return decorator
