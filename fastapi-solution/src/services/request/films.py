from typing import List, Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.movie import Movie
from services.request_service import RequestManyService


# TODO: определиться с названием film/movie везде по разному
class FilmsRequestService(RequestManyService):
    # TODO: вынести название индекса в глодальные настройки приложения
    elastic_index = "movies"

    async def get_films_from_elastic(self, edsl_query: Optional[dict] = None) -> Optional[List[Movie]]:
        try:
            return self._hits_to_model_list(
                List[Movie], await self.elastic.search(index=self.elastic_index, body=edsl_query)
            )
        except NotFoundError:
            return None


# TODO: для чего используется lru_cache?
@lru_cache()
def get_films_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmsRequestService:
    return FilmsRequestService(redis, elastic)
