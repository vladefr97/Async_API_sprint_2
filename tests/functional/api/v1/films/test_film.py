from http import HTTPStatus

import pytest
from functional.api.settings import FILMS_V1_URL
from functional.api.types import AsyncGET
from functional.factories.films import FakeFilm


class TestFilm:
    @pytest.mark.asyncio
    async def test_search_detailed(self, make_get_request: AsyncGET, fake_film: FakeFilm):
        response = await make_get_request(FILMS_V1_URL + str(fake_film.id))
        assert response.status == HTTPStatus.OK
        assert response.body["id"] == str(fake_film.id)

    @pytest.mark.asyncio
    async def test_search_detailed_with_bad_id(self, make_get_request: AsyncGET, fake_film: FakeFilm):
        response = await make_get_request(FILMS_V1_URL + str(fake_film.id) + "bad")
        assert response.status == HTTPStatus.NOT_FOUND
