import asyncio
import time

import aiohttp
import aioredis
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

from .utils.elastic_utils import test_data_set

SERVICE_URL = 'http://127.0.0.1:8000/api/v1/'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='function')
def restore_es():
    test_data_set()


@pytest.fixture(scope='function')
async def redis_clean():
    client = await aioredis.create_redis_pool(('127.0.0.1', 6379))
    await client.flushall(async_op=True)
    time.sleep(0.5)
    yield client.close()


@pytest.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture(scope='function')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='function')
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
