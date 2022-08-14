from typing import Optional

from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.genre import Genre
from services.dependence.cache import AsyncCacheStorage
from services.dependence.search import AsyncSearchStorage
from services.request_service import RequestSingleService


class GenreService(RequestSingleService):
    index_name = "genre"

    def __init__(self, cache: AsyncCacheStorage, search: AsyncSearchStorage, expire: Optional[int] = None):
        super().__init__(cache, search)
        if expire:
            self.expire = expire

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_search(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre

    async def _get_genre_from_search(self, genre_id: str) -> Optional[Genre]:
        return await self._get_from_search(genre_id, Genre)

    async def _genre_from_cache(self, genre_id: str) -> Optional[Genre]:
        key = "genre" + ":" + str(genre_id)
        return await self._get_from_cache(key, Genre)

    async def _put_genre_to_cache(self, genre: Genre) -> None:
        key = "genre" + ":" + str(genre.id)
        await self._put_to_cache(key, genre.json(), self.expire)


@lru_cache()
def get_genre_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    search: AsyncSearchStorage = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, search)
