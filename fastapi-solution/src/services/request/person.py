from typing import Optional

from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.entities.film_person import FilmPerson
from services.request_service import RequestSingleService

PERSON_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class PersonService(RequestSingleService):
    index_name = "person"

    async def get_by_id(self, person_id: str) -> Optional[FilmPerson]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)

        return person

    async def _get_person_from_elastic(self, person_id: str) -> Optional[FilmPerson]:
        return await self._get_from_elastic(person_id, FilmPerson)

    async def _person_from_cache(self, person_id: str) -> Optional[FilmPerson]:
        key = "person" + ":" + str(person_id)
        return await self._get_from_cache(key, FilmPerson)

    async def _put_person_to_cache(self, person: FilmPerson) -> None:
        key = "person" + ":" + str(person.id)
        await self._put_to_cache(key, person.json(), PERSON_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
