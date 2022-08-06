from typing import List, Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.film_person import FilmPerson
from services.request_service import RequestManyService


class PersonsRequestService(RequestManyService):
    elastic_index = "person"

    async def get_persons(self, edsl_query: Optional[dict] = None) -> Optional[List[FilmPerson]]:
        try:
            return self._hits_to_model_list(
                List[FilmPerson], await self.elastic.search(index=self.elastic_index, body=edsl_query)
            )
        except NotFoundError:
            return None


@lru_cache()
def get_persons_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonsRequestService:
    return PersonsRequestService(redis, elastic)
