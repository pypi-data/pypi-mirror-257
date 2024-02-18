from collections.abc import Generator
from pathlib import Path
from unittest.mock import patch

import pytest
from aioresponses import aioresponses

from aglog import dict_config_from_yaml

test_root = Path(__file__).parent


def pytest_addoption(parser):
    parser.addoption("--debug-log", action="store_true", help="Enable debug logging")


@pytest.fixture(scope="session")
def debug_log(request):
    return request.config.getoption("--debug-log")


@pytest.fixture(scope="session", autouse=True)
def _setup_logging(debug_log) -> None:
    if debug_log:
        dict_config_from_yaml(test_root / "logging_conf.yaml")


class MockResponse:
    def __init__(self, status: int, json: dict):
        self.status = status
        self._json = json

    async def json(self):
        return self._json

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.fixture()
def mock_aiohttp_post(self, method, url, **kwargs):
    with patch("aiohttp.ClientSession.post") as mock:
        yield mock


@pytest.fixture()
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    with aioresponses() as m:
        yield m
