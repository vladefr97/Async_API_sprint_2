from typing import List, Optional

from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.genre import Genre
from services.dependence.cache import AsyncCacheStorage
from services.dependence.search import AsyncSearchStorage
from services.request_service import RequestManyService


class GenresRequestService(RequestManyService):
    index_name = "genre"

    async def get_genres(self, edsl_query: Optional[dict] = None) -> Optional[List[Genre]]:
        return self._hits_to_model_list(
            List[Genre], await self.search.search(index=self.index_name, body=edsl_query)
        )


@lru_cache()
def get_genres_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        search: AsyncSearchStorage = Depends(get_elastic),
) -> GenresRequestService:
    return GenresRequestService(cache, search)
