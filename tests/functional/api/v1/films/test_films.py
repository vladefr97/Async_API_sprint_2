from http import HTTPStatus

import pytest
from functional.api.settings import FILMS_V1_URL
from functional.api.types import AsyncGET
from functional.models.entities.movie import Movie


@pytest.mark.asyncio
class TestFilms:

    async def test_films_response_size(self, make_get_request: AsyncGET):
        RESPONSE_SIZE = 5
        query_param = {"filter[size]": RESPONSE_SIZE}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == RESPONSE_SIZE

    async def test_films_search_with_desc_sorting(self, make_get_request: AsyncGET):
        first_film, second_film, third_film = await self.__get_three_sorted_films(make_get_request, "-imdb_rating")
        assert first_film.imdb_rating > second_film.imdb_rating > third_film.imdb_rating

    async def test_films_search_with_asc_sorting(self, make_get_request: AsyncGET):
        first_film, second_film, third_film = await self.__get_three_sorted_films(make_get_request, "imdb_rating")
        assert first_film.imdb_rating < second_film.imdb_rating < third_film.imdb_rating

    async def __get_three_sorted_films(self, make_get_request: AsyncGET, sorting: str):
        response_size = 3
        query_param = {"filter[size]": response_size, "sort": sorting}
        response = await make_get_request(FILMS_V1_URL, query_param)
        first_film = Movie(**response.body[0])
        second_film = Movie(**response.body[1])
        third_film = Movie(**response.body[2])
        return first_film, second_film, third_film

    async def test_films_search_by_actor_name(self, make_get_request: AsyncGET, fake_film: Movie):
        fake_actor_name = fake_film.actors[0].name
        query_param = {"filter[in_actors]": fake_actor_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body)

        fake_actor_name = "__badname__"
        query_param = {"filter[in_writers]": fake_actor_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.NOT_FOUND

    async def test_films_search_by_writer_name(self, make_get_request: AsyncGET, fake_film: Movie):
        fake_writer_name = fake_film.writers[0].name
        query_param = {"filter[in_writers]": fake_writer_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body)

        fake_writer_name = "__badname__"
        query_param = {"filter[in_writers]": fake_writer_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.NOT_FOUND

    async def test_films_search_by_director_name(self, make_get_request: AsyncGET, fake_film: Movie):
        fake_director_name = fake_film.directors[0]
        query_param = {"filter[in_directors]": fake_director_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body)

        fake_director_name = "__badname__"
        query_param = {"filter[in_writers]": fake_director_name}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.NOT_FOUND
