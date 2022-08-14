from typing import List, Optional

from functools import lru_cache
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.movie import Movie
from services.dependence.cache import AsyncCacheStorage
from services.dependence.search import AsyncSearchStorage
from services.request_service import RequestManyService


# TODO: определиться с названием film/movie везде по разному
class FilmsRequestService(RequestManyService):
    # TODO: вынести название индекса в глодальные настройки приложения
    index_name = "movies"

    async def get_films(self, edsl_query: Optional[dict] = None) -> Optional[List[Movie]]:
        return self._hits_to_model_list(
            List[Movie], await self.search.search(index=self.index_name, body=edsl_query)
        )


@lru_cache()
def get_films_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        search: AsyncSearchStorage = Depends(get_elastic),
) -> FilmsRequestService:
    return FilmsRequestService(cache, search)
