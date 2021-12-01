import pytest

from .models import ShortFilm


@pytest.mark.asyncio
async def test_films_search(make_get_request):
    response = await make_get_request('film', params={'search': 'Star Wars'})

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'


@pytest.mark.asyncio
async def test_persons_search(make_get_request):
    response = await make_get_request('person', params={'search': 'ford'})

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'


@pytest.mark.asyncio
async def test_persons_film_search(make_get_request):
    response = await make_get_request('person/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1/film')

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert ShortFilm(**response.body[0]), 'Неправильная структура полей и/или типов в фильме'
