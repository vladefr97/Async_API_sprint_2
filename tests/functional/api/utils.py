from typing import List

from elasticsearch import AsyncElasticsearch
from tests.factories.films import ElasticFakeFilm
from tests.factories.genres import ElasticFakeGenre
from tests.functional.api.settings import MOVIES_INDEX_NAME, GENRES_INDEX_NAME

from models.entities.movie import Movie


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

    return await es_client.bulk(
        body=request_body,
    )