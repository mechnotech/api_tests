import pytest


@pytest.mark.asyncio
async def test_page_intersection(make_get_request):
    first_page = await make_get_request('film', params={'page[size]': 10, 'page[number]': 1})
    second_page = await make_get_request('film', params={'page[size]': 10, 'page[number]': 2})
    first_page = set([x['id'] for x in first_page.body])
    second_page = set([x['id'] for x in second_page.body])
    assert first_page & second_page == set(), 'Следующая страница повторяет содержимое предыдущей'


@pytest.mark.asyncio
async def test_page_lose_items(make_get_request):
    first_page = await make_get_request('film', params={'page[size]': 5, 'page[number]': 1})
    second_page = await make_get_request('film', params={'page[size]': 5, 'page[number]': 2})
    third_page = await make_get_request('film', params={'page[size]': 10, 'page[number]': 1})
    first_page = set([x['id'] for x in first_page.body])
    second_page = set([x['id'] for x in second_page.body])
    third_page = set([x['id'] for x in third_page.body])
    content = first_page | second_page
    assert (content - third_page) == set(), 'Страницы пропускают контент'


@pytest.mark.asyncio
async def test_page_out_of_range(make_get_request):
    responce = await make_get_request('film', params={'page[size]': 50, 'page[number]': 1000})
    assert responce.status == 404, f'Ожидается 404, запрос вернул {responce.status}'


@pytest.mark.asyncio
async def test_page_zero_size(make_get_request):
    responce = await make_get_request('film', params={'page[size]': 0, 'page[number]': 0})
    assert responce.status == 404, f'Ожидается 404, запрос вернул {responce.status}'


@pytest.mark.asyncio
async def test_page_wrong_params(make_get_request):
    responce = await make_get_request('film', params={'page[size]': 'ten', 'page[number]': 'first'})
    assert responce.status == 400, f'Ожидается 400 (Bad request), запрос вернул {responce.status}'
