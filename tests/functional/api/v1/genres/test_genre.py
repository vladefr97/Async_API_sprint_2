from http import HTTPStatus

import pytest

from tests.factories.genres import FakeGenre
from tests.functional.api.settings import GENRES_V1_URL
from tests.functional.api.types import AsyncGET
from typing import List


class TestGenre:
    # @pytest.mark.asyncio
    # async def test_search_detailed(self, make_get_request: AsyncGET, fake_genre: FakeGenre):
    #     response = await make_get_request(GENRES_V1_URL + str(fake_genre.id))
    #     assert response.status == HTTPStatus.OK
    #     assert response.body["id"] == str(fake_genre.id)
    @pytest.mark.asyncio
    async def test_search_detailed(self, make_get_request: AsyncGET, fake_genres: List[FakeGenre]):
        response = await make_get_request(GENRES_V1_URL + str(fake_genres[0].id))
        assert response.status == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_search_detailed_with_bad_id(self, make_get_request: AsyncGET, fake_genres: List[FakeGenre]):
        response = await make_get_request(GENRES_V1_URL + str(fake_genres[0].id) + "bad")
        assert response.status == HTTPStatus.NOT_FOUND
