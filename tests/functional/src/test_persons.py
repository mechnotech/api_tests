import pytest

from .models import Person, ShortPerson, test_set


@pytest.mark.asyncio
async def test_person_by_id(make_get_request):
    response = await make_get_request(f'person/{test_set.person_id}')
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, dict), 'Ожидается dict в ответе'
    assert Person(**response.body), 'Неправильная структура полей и/или типов в Персоне'


@pytest.mark.asyncio
async def test_person_cache(make_get_request, es_client, restore_es):
    old_response = await make_get_request(f'person/{test_set.person_id}')
    await es_client.delete(index='persons', id=test_set.person_id)
    response = await make_get_request(f'person/{test_set.person_id}')
    assert response.status == 200, f'Кэш redis не сработал! Ответ {response.status}, ожидался: 200'
    assert old_response == response, f'Кэш вернул не тот объект: {old_response} и {response}'


@pytest.mark.asyncio
async def test_persons_list_all(make_get_request, restore_es):
    response = await make_get_request('person', params={'page[size]': 5000, 'page[number]': 0})
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert len(response.body) == 4166, 'Запрос должен вернуть 4166 записей'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert ShortPerson(**response.body[0]), 'Неправильная структура полей и/или типов в Персоне'


@pytest.mark.asyncio
async def test_genre_404(make_get_request):
    response = await make_get_request(f'person/{test_set.wrong_id}')
    assert response.status == 404, f'Ответ {response.status}, ожидался: 404'





