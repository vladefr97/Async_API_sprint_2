# TODO: файл не должен лежать на одном уровне с film и person
from typing import Any, Dict, List, Optional, Type

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from pydantic import BaseModel, parse_obj_as


class RequestService:
    index_name = ""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic


class RequestSingleService(RequestService):
    async def _get_from_elastic(self, object_id: str, object_model: Type[BaseModel]) -> Optional[BaseModel]:
        try:
            return object_model(**(await self.elastic.get(self.index_name, object_id))["_source"])
        except NotFoundError:
            return None

    async def _get_from_cache(self, object_id: str, object_model: Type[BaseModel]) -> Any:
        data = await self.redis.get(object_id)
        if not data:
            return None
        return object_model.parse_raw(data)

    async def _put_to_cache(self, object_id: str, object_json: str, cache_expires: int) -> None:
        await self.redis.set(object_id, object_json, expire=cache_expires)


class RequestManyService(RequestService):
    def _hits_to_model_list(self, list_model: Type[List[BaseModel]], es_docs: Dict[str, Any]) -> List[BaseModel]:
        values_dict = [item["_source"] for item in es_docs["hits"]["hits"]]
        objs = parse_obj_as(list_model, values_dict)
        return objs
