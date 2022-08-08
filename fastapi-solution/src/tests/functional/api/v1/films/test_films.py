# Film
# Получение фильма по правильному id
# Получение фильма по неправильному id
from typing import Callable, Dict, Union, Awaitable

import pytest
from http import HTTPStatus
from models.entities.movie import Movie
from tests.functional.api.settings import FILMS_V1_URL

# TODO: виды тестов
# Films
# Получение фильма по id
# Фильтрация с неправильно заданным рейтингом (больше максимально возможного, меньше минимального, строка)
# Фильтрация по жанру фильма (должен быть как минимум один)
# Фильтрация по актерам фильма (должен быть как минимум один)
# Фильтрация по режиссерам фильма (должен быть как минимум один)
# Фильтрация по сценаристам фильма (должен быть как минимум один)
# Фильтрация страницы и размера (при размере 5, должно быть как минимум две страницы)
# Проверка сортировки
AsyncGET = Callable[[str, Dict[str, Union[str, float]]], Awaitable]


class TestFilms:

    @pytest.mark.asyncio
    async def test_films_response_size(self, make_get_request: AsyncGET):
        RESPONSE_SIZE = 5
        query_param = {'filter[size]': RESPONSE_SIZE}
        response = await make_get_request(FILMS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == RESPONSE_SIZE

    @pytest.mark.asyncio
    async def test_films_search_with_desc_sorting(self, make_get_request: AsyncGET):
        first_film, second_film, third_film = await self.__get_three_sorted_films(make_get_request, '-imdb_rating')
        assert first_film.imdb_rating > second_film.imdb_rating > third_film.imdb_rating

    @pytest.mark.asyncio
    async def test_films_search_with_asc_sorting(self, make_get_request: AsyncGET):
        first_film, second_film, third_film = await self.__get_three_sorted_films(make_get_request, 'imdb_rating')
        assert first_film.imdb_rating < second_film.imdb_rating < third_film.imdb_rating

    async def __get_three_sorted_films(self, make_get_request: AsyncGET, sorting: str):
        response_size = 3
        query_param = {'filter[size]': response_size, 'sort': sorting}
        response = await make_get_request(FILMS_V1_URL, query_param)
        first_film = Movie(**response.body[0])
        second_film = Movie(**response.body[1])
        third_film = Movie(**response.body[2])
        return first_film, second_film, third_film
