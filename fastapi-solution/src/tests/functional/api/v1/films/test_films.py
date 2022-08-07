from typing import List

import pytest
from tests.functional.api.settings import FILMS_V1_URL

from models.entities.movie import Movie

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

# Film
# Получение фильма по правильному id
# Получение фильма по неправильному id


class TestFilms:
    @pytest.mark.asyncio
    async def test_search_detailed(self, es_client, make_get_request, fake_films: List[Movie]):

        # Выполнение запроса
        response = await make_get_request(FILMS_V1_URL, {"filter[imdb_rating_lt]": 8, "filter[imdb_rating_gt]": 7})

        # Проверка результата
        assert response.status == 200
