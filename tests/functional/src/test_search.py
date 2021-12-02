import pytest

from .models import ShortFilm, test_set


@pytest.mark.asyncio
async def test_films_search(make_get_request):
    response = await make_get_request('film/search', params={'query': test_set.film_search_phrase})

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'


@pytest.mark.asyncio
async def test_persons_search(make_get_request):
    response = await make_get_request('person/search', params={'query': test_set.person_search_phrase})

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка персон подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'


@pytest.mark.asyncio
async def test_persons_search_limit(make_get_request):
    response = await make_get_request(
        'person/search',
        params={'query': test_set.person_search_phrase,
                'page[size]': 5
                }
    )
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) == 5, 'Размер страницы должен быть 5 записей'


@pytest.mark.asyncio
async def test_persons_search_limit(make_get_request):
    response = await make_get_request(
        'person/search',
        params={'query': test_set.person_search_phrase,
                'page[size]': 1
                }
    )
    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    full_name = response.body[0]['full_name']
    assert (
        test_set.person_search_phrase.lower() in full_name.lower(),
        'Релевантность поиска нарушена, в выдаче нет искомого'
    )


@pytest.mark.asyncio
async def test_persons_film_search(make_get_request):
    response = await make_get_request(f'person/{test_set.person_id}/film')

    assert response.status == 200, f'Ответ {response.status}, ожидался: 200'
    assert len(response.body) > 1, 'Длина списка фильмов подозрительно маленькая (должна быть больше 1)'
    assert isinstance(response.body, list), 'Возвращается не список (list)'
    assert ShortFilm(**response.body[0]), 'Неправильная структура полей и/или типов в фильме'
