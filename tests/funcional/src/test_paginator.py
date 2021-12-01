import pytest


@pytest.mark.asyncio
async def test_paginator_borders(make_get_request):
    first_page = await make_get_request('film', params={'page[size]': 10, 'page[number]': 1})
    second_page = await make_get_request('film', params={'page[size]': 10, 'page[number]': 2})
    first_page = set([x['id'] for x in first_page.body])
    second_page = set([x['id'] for x in second_page.body])
    assert first_page & second_page == set(), 'Следующая страница повторяет содержимое предыдущей'
