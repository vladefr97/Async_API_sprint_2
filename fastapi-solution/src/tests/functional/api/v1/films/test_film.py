from http import HTTPStatus

import pytest
from tests.functional.api.settings import FILMS_V1_URL

from models.entities.movie import Movie


class TestFilm:
    @pytest.mark.asyncio
    async def test_search_detailed(self, make_get_request, fake_film: Movie):
        response = await make_get_request(FILMS_V1_URL + str(fake_film.id))
        assert response.status == HTTPStatus.OK
        assert response.body["id"] == str(fake_film.id)

    @pytest.mark.asyncio
    async def test_search_detailed_with_bad_id(self, make_get_request, fake_film: Movie):
        response = await make_get_request(FILMS_V1_URL + str(fake_film.id) + "bad")
        assert response.status == HTTPStatus.NOT_FOUND
