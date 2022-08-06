from typing import List, Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.genre import Genre
from services.request_service import RequestManyService


class GenresRequestService(RequestManyService):
    elastic_index = "genre"

    async def get_genres(self, edsl_query: Optional[dict] = None) -> Optional[List[Genre]]:
        try:
            return self._hits_to_model_list(
                List[Genre], await self.elastic.search(index=self.elastic_index, body=edsl_query)
            )
        except NotFoundError:
            return None


@lru_cache()
def get_genres_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenresRequestService:
    return GenresRequestService(redis, elastic)
