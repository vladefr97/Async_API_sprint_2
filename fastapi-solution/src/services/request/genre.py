from typing import Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.genre import Genre
from services.request_service import RequestSingleService

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class GenreService(RequestSingleService):
    index_name = "genre"

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[Genre]:
        return await self._get_from_elastic(genre_id, Genre)

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        key = "genre" + ":" + str(genre_id)
        return await self._get_from_cache(key, Genre)

    async def _put_genre_to_cache(self, genre: Genre) -> None:
        key = "genre" + ":" + str(genre.id)
        await self._put_to_cache(key, genre.json(), GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
