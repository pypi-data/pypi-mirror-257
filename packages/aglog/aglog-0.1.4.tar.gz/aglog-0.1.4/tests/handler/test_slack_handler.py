import logging
import time
from unittest.mock import MagicMock, patch

import pytest
from aioresponses import CallbackResult, aioresponses

from aglog.handler import slack_handler as target

request: target.Request | None = None


@pytest.fixture()
def emit_patch_slack_handler():
    def set_request(self: target.HTTPHandler, record: logging.LogRecord):
        global request  # noqa: PLW0603
        request = self.get_request(record)

    with patch("aglog.handler.SlackHandler.emit", new=set_request):
        handler = target.SlackHandler(token="test", channel="channel")  # noqa: S106
        yield handler


@pytest.fixture()
def logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    yield logger
    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()
    logger.level = logging.WARN


@pytest.fixture()
def emit_patch_logger(emit_patch_slack_handler, logger: logging.Logger):
    logger.addHandler(emit_patch_slack_handler)
    return logger


@pytest.fixture()
def aiohttp_patch_slack_handler():
    with patch("aiohttp.ClientSession._request") as mock:
        yield mock


def test_slack_handler(emit_patch_logger: logging.Logger):
    emit_patch_logger.info("test")
    assert request is not None
    assert request.method == "POST"
    assert request.url == target.SlackHandler.URL
    assert request.headers == {"Authorization": "Bearer test"}
    assert request.json is not None
    assert request.json["attachments"][0]["color"] == "good"

    emit_patch_logger.exception("test")
    assert request is not None
    assert request.json["attachments"][0]["color"] == "#E91E63"

    emit_patch_logger.critical("test", stack_info=True)
    assert request is not None
    assert request.json["attachments"][0]["color"] == "danger"


@patch.object(target.SlackHandler, "retry_delay", 0)
@patch.object(target.SlackHandler, "retry_attempts", 2)
def test_slack_handler_exception(mock_aioresponse: aioresponses, logger: logging.Logger):
    mock = MagicMock(return_value=CallbackResult(status=404, reason="test"))
    mock_aioresponse.post(target.SlackHandler.URL, callback=mock, repeat=True)

    handler = target.SlackHandler(token="test", channel="channel", rate_limit=100)  # noqa: S106
    logger.addHandler(handler)
    logger.info("test")
    handler.close()
    assert mock.call_count == target.SlackHandler.retry_attempts


@patch.object(target.SlackHandler, "retry_delay", 0)
@patch.object(target.SlackHandler, "retry_attempts", 2)
def test_slack_handler_exception2(mock_aioresponse: aioresponses, logger: logging.Logger):
    mock = MagicMock(return_value=CallbackResult(status=200, payload={"ok": True}))
    mock_aioresponse.post(target.SlackHandler.URL, callback=mock)
    handler = target.SlackHandler(token="test", channel="channel", rate_limit=100)  # noqa: S106
    logger.addHandler(handler)
    logger.info("test")
    time.sleep(0.03)
    assert mock.call_count == 1

    mock = MagicMock(return_value=CallbackResult(status=200, payload={"error": "test"}))
    mock_aioresponse.post(target.SlackHandler.URL, callback=mock, repeat=True)
    logger.info("test")
    handler.close()
    assert mock.call_count == target.SlackHandler.retry_attempts
