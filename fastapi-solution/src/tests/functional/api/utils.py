from typing import List

from elasticsearch import AsyncElasticsearch
from tests.functional.api.settings import MOVIES_INDEX_NAME

from models.entities.movie import Movie


def check_es_indexes_exists(client: AsyncElasticsearch):
    if not client.indices.exists(index=MOVIES_INDEX_NAME):
        raise ConnectionError(f"Elasticsearch index '{MOVIES_INDEX_NAME}' does not exists!")


async def load_fake_films(es_client: AsyncElasticsearch, fake_films: List[Movie]):
    request_body = []
    for film in fake_films:
        request_body.append({"index": {"_index": MOVIES_INDEX_NAME, "_id": film.id}})
        request_body.append(film.dict(by_alias=True))

    return await es_client.bulk(
        body=request_body,
    )
