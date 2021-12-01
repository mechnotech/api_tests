import pytest

from .models import FilmStructure, ShortFilmStructure




@pytest.mark.asyncio
async def test_get_film_detail_by_id(make_get_request, restore_es):
    response = await make_get_request('film/317df96f-2cbc-48fd-98ba-16a94cac68a0')
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, dict), 'Ожидается dict'
    assert FilmStructure(**response.body), 'Неправильная структура полей и/или типов в фильме'


@pytest.mark.asyncio
async def test_find_all(make_get_request, redis_clean, restore_es):
    response = await make_get_request('film', params={'page[size]': 5000, 'page[number]': 0})
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert len(response.body) == 999, 'Запрос должен вернуть 999 записей'


@pytest.mark.asyncio
async def test_cache_work(es_client, make_get_request):
    old_response = await make_get_request('film/317df96f-2cbc-48fd-98ba-16a94cac68a0')
    await es_client.delete(index='movies', id='317df96f-2cbc-48fd-98ba-16a94cac68a0')
    response = await make_get_request('film/317df96f-2cbc-48fd-98ba-16a94cac68a0')
    assert response.status == 200, f'Кэш redis не сработал! Ответ {response.status}, ожидался: 200'
    assert old_response == response, f'Кэш вернул не тот объект: {old_response} и {response}'


@pytest.mark.asyncio
async def test_404_film(make_get_request):
    response = await make_get_request('film/3172396f-2cbc-48fd-98ba-16a943ac68a0')
    assert response.status == 404, f'Ответ {response.status}, ожидался: 404'


@pytest.mark.asyncio
async def test_films_search(make_get_request):
    response = await make_get_request('film', params={'search': 'Star Wars'})

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    one = response.body[0]
    assert ShortFilmStructure(**one), 'Неправильная структура полей и/или типов в фильме'
