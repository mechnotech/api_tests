from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .utils.elastic_utils import apply_test_set
from .settings import config, SERVICE_URL


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='function')
def restore_es():
    apply_test_set()


@pytest.fixture(scope='function')
async def redis_clean():
    client = await aioredis.create_redis_pool((config.redis_host, config.redis_port))
    await client.flushall(async_op=True)
    client.close()


@pytest.fixture(scope='function')
async def es_client():
    client = AsyncElasticsearch(hosts=[f'{config.es_host}:{config.es_port}'])
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
