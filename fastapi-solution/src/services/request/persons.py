from typing import List, Optional

from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.film_person import FilmPerson
from services.dependence.cache import AsyncCacheStorage
from services.dependence.search import AsyncSearchStorage
from services.request_service import RequestManyService


class PersonsRequestService(RequestManyService):
    index_name = "person"

    async def get_persons(self, edsl_query: Optional[dict] = None) -> Optional[List[FilmPerson]]:
        return self._hits_to_model_list(
            List[FilmPerson], await self.search.search(index=self.index_name, body=edsl_query)
        )


@lru_cache()
def get_persons_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        search: AsyncSearchStorage = Depends(get_elastic),
) -> PersonsRequestService:
    return PersonsRequestService(cache, search)
