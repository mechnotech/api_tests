import aiohttp
import pytest

from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

SERVICE_URL = 'http://127.0.0.1:8000/api/v1/'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='function')
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + '/api/v1' + method  # в боевых системах старайтесь так не делать!
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.mark.asyncio
async def test_search(session):
    # Заполнение данных для теста
    #await es_client.bulk(body)

    # Выполнение запроса
    #response = await make_get_request('/search', {'search': 'Star Wars'})
    response = await session.get(SERVICE_URL + 'film', params={'search': 'Star Wars'})
    response = HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    # Проверка результата
    assert response.status == 200
    assert len(response.body) > 1
    assert isinstance(response.body, list)
    assert isinstance(response.body, list)
    one = response.body[0]
    assert one.get('id')
    assert one.get('title')
    assert one.get('imdb_ratin')
    assert isinstance(one['imdb_rating'], float)
