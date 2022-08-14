from typing import List

from elasticsearch import AsyncElasticsearch

from functional.api.settings import GENRES_INDEX_NAME, MOVIES_INDEX_NAME, PERSON_INDEX_NAME
from functional.factories.films import ElasticFakeFilm
from functional.factories.genres import ElasticFakeGenre
from functional.factories.persons import ElasticFakePerson


def check_es_indexes_exists(client: AsyncElasticsearch):
    if not client.indices.exists(index=MOVIES_INDEX_NAME):
        raise ConnectionError(f"Elasticsearch index '{MOVIES_INDEX_NAME}' does not exists!")


async def load_fake_films(es_client: AsyncElasticsearch, fake_films: List[ElasticFakeFilm]):
    request_body = []
    for film in fake_films:
        request_body.append({"index": {"_index": MOVIES_INDEX_NAME, "_id": film.id}})
        request_body.append(film.dict(by_alias=True))

    return await es_client.bulk(
        body=request_body,
    )


async def load_fake_genres(es_client: AsyncElasticsearch, fake_genres: List[ElasticFakeGenre]):
    request_body = []
    for genre in fake_genres:
        request_body.append({"index": {"_index": GENRES_INDEX_NAME, "_id": genre.id}})
        request_body.append(genre.dict(by_alias=True))

    response = await es_client.bulk(
        body=request_body,
    )
    return response


async def load_fake_persons(es_client: AsyncElasticsearch, fake_persons: List[ElasticFakePerson]):
    request_body = []
    for person in fake_persons:
        request_body.append({"index": {"_index": PERSON_INDEX_NAME, "_id": person.id}})
        request_body.append(person.dict(by_alias=True))

    response = await es_client.bulk(
        body=request_body,
    )
    return response
