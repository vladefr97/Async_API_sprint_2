from http import HTTPStatus

import pytest
from functional.api.settings import FILMS_V1_URL
from functional.api.types import AsyncGET
from functional.factories.films import FakeFilm


@pytest.mark.asyncio
class TestFilm:

    async def test_search_detailed(self, make_get_request: AsyncGET, fake_film: FakeFilm):
        request_url = FILMS_V1_URL + str(fake_film.id)

        response = await make_get_request(request_url)

        assert response.status == HTTPStatus.OK
        assert response.body["id"] == str(fake_film.id)

    async def test_search_detailed_with_bad_id(self, make_get_request: AsyncGET, fake_film: FakeFilm):
        request_url = FILMS_V1_URL + str(fake_film.id) + "bad"

        response = await make_get_request(request_url)

        assert response.status == HTTPStatus.NOT_FOUND
