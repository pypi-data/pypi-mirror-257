import aiohttp
import pytest
from aioresponses import aioresponses

import aglog.utils.request_backend as target


def test_request_backend():
    target.RequestBackend(name="test1")
    target.RequestBackend(name="test2")
    assert len(target.RequestBackend._singleton) == 2

    target.RequestBackend(name="test1")
    assert len(target.RequestBackend._singleton) == 2


@pytest.mark.asyncio()
async def test_http_client(mock_aioresponse: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = target.HttpClient(session=session)
        url = "http://test.com"
        mock_aioresponse.get(url, status=200, payload={"test": "test"})
        await client.send(target.Request(method="GET", url=url))

        mock_aioresponse.post(url, status=200, payload={"test": "test"})
        await client.send(target.Request(method="POST", url=url))

        mock_aioresponse.put(url, status=200, payload={"test": "test"})
        with pytest.raises(ValueError, match="Invalid method: PUT"):
            await client.send(target.Request(method="PUT", url=url))

        async def handler(response):
            res = await response.json()
            assert res == {"test": "test"}

        mock_aioresponse.get(url, status=200, payload={"test": "test"})
        client = target.HttpClient(session=session, http_response_handler=handler)
        await client.send(target.Request(method="GET", url=url))
