from typing import Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.movie import Movie
from services.request_service import RequestSingleService

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


# TODO: нужно доработать, чтобы работал с сериалами и фильмами
class FilmService(RequestSingleService):
    index_name = "movies"

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[Movie]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film = await self._film_from_cache(film_id)
        if not film:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film = await self._get_film_from_elastic(film_id)
            if not film:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм в кеш
            await self._put_film_to_cache(film)

        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Movie]:
        return await self._get_from_elastic(film_id, Movie)

    async def _film_from_cache(self, film_id: str) -> Optional[Movie]:
        key = "film" + ":" + str(film_id)
        return await self._get_from_cache(key, Movie)

    async def _put_film_to_cache(self, film: Movie) -> None:
        key = "film" + ":" + str(film.id)
        await self._put_to_cache(key, film.json(), FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
