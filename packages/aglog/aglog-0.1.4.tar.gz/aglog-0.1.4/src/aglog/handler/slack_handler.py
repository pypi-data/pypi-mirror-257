import logging
from http import HTTPStatus

import aiohttp
from typing_extensions import Self, override

from aglog.formatter.iso8601_formatter import Iso8601Formatter
from aglog.utils.request_backend import Request

from .web_handler import HTTPHandler

logger = logging.getLogger(__name__)


class SlackRetryError(Exception):
    pass


class SlackHandler(HTTPHandler):
    URL = "https://slack.com/api/chat.postMessage"
    retry_exceptions: tuple[type[BaseException], ...] = (aiohttp.ClientError, SlackRetryError)
    retry_attempts: int = 3
    retry_delay: float = 0.01

    def __init__(  # noqa: PLR0913
        self: Self,
        token: str,
        channel: str,
        stop_timeout: float = 60.0,
        rate_limit: int = 1,
        formatter: logging.Formatter | None = None,
        footer_formatter: logging.Formatter | None = None,
        level: int = logging.NOTSET,
    ) -> None:
        """SlackHandler

        Args:
            token (str): slack token.
            channel (str): slack channel name or id.
            stop_timeout (float, optional): gracefull stop timeout. Defaults to 60.0.
            rate_limit (int, optional): rate limit per second. Defaults to 1.
            formatter (logging.Formatter | None, optional): main formatter. Defaults to None.
            footer_formatter (logging.Formatter | None, optional): footer formatter. Defaults to None.
            level (int, optional): log level. Defaults to logging.NOTSET.
        """
        self.channel = channel
        self.footer_formatter = footer_formatter or Iso8601Formatter(fmt="%(asctime)s", datefmt="milliseconds")
        self.headers = {"Authorization": f"Bearer {token}"}
        super().__init__(
            stop_timeout=stop_timeout,
            rate_limit=rate_limit,
            level=level,
            formatter=formatter or Iso8601Formatter(),
        )

    @override
    def get_request(self: Self, record: logging.LogRecord) -> Request:
        return Request(
            method="POST",
            url=self.URL,
            headers=self.headers,
            json=self.map_log_record(record),
        )

    def map_log_record(self: Self, record: logging.LogRecord) -> dict:
        loglevel_color = {
            "DEBUG": "#2196F3",
            "INFO": "good",
            "WARNING": "warning",
            "ERROR": "#E91E63",
            "CRITICAL": "danger",
        }
        text = self.format(record)
        other_info = get_exc_info_or_stack_info(record)
        if other_info is not None:
            text += "\n" + f"```{other_info}```"

        content = {
            "ts": record.created,
            "text": text,
            "color": loglevel_color.get(record.levelname, "#FFFFFF"),
            "footer": format_footer(record, self.footer_formatter),
        }

        return {"attachments": [content], "channel": self.channel}

    @override
    async def http_response_handler(self: Self, response: aiohttp.ClientResponse) -> None:
        if response.status != HTTPStatus.OK:
            response.raise_for_status()
        data = await response.json()
        if data.get("ok", False):
            return
        error = data.get("error")
        if error is None:
            return  # pragma: no cover
        raise SlackRetryError(error)


def format_footer(record: logging.LogRecord, formatter: logging.Formatter) -> str:
    record.exc_info = None
    record.stack_info = None
    record.exc_text = None
    return formatter.format(record)


def get_exc_info_or_stack_info(record: logging.LogRecord) -> str | None:
    if record.exc_info is not None:
        return logging.Formatter().formatException(record.exc_info)
    if record.stack_info is not None:
        return logging.Formatter().formatStack(record.stack_info)
    return None
