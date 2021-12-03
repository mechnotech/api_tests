import pytest

from .models import Film, ShortFilm, test_set

@pytest.mark.asyncio
async def test_get_film_detail_by_id(make_get_request, restore_es):
    response = await make_get_request(f'film/{test_set.film_id}')
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, dict), 'Ожидается dict в ответе'
    assert Film(**response.body), 'Неправильная структура полей и/или типов в фильме'


@pytest.mark.asyncio
async def test_films_list_all(make_get_request, redis_clean, restore_es):
    response = await make_get_request('film', params={'page[size]': 5000, 'page[number]': 0})
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert len(response.body) == 999, 'Запрос должен вернуть 999 записей'
    assert ShortFilm(**response.body[0]), 'Неправильная структура полей и/или типов в фильме'


@pytest.mark.asyncio
async def test_cache_work(es_client, make_get_request):
    old_response = await make_get_request(f'film/{test_set.film_id}')
    await es_client.delete(index='movies', id=test_set.film_id)
    response = await make_get_request(f'film/{test_set.film_id}')
    assert response.status == 200, f'Кэш redis не сработал! Ответ {response.status}, ожидался: 200'
    assert old_response == response, f'Кэш вернул не тот объект: {old_response} и {response}'


@pytest.mark.asyncio
async def test_404_film(make_get_request):
    response = await make_get_request(f'film/{test_set.wrong_id}')
    assert response.status == 404, f'Ответ {response.status}, ожидался: 404'

