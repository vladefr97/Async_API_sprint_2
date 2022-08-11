from typing import List, Optional

from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
from tests.factories.films import FilmFactory, get_fake_elastic_films, get_pretty_fake_films
from tests.functional.api.settings import ES_HOST, MOVIES_INDEX_NAME
from tests.functional.api.utils import check_es_indexes_exists, load_fake_films

from models.entities.movie import Movie


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="function")
async def es_client():
    client = AsyncElasticsearch(hosts=ES_HOST)
    check_es_indexes_exists(client)
    yield client
    await client.close()


@pytest.fixture(scope="function")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="function")
def make_get_request(session):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}

        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


# TODO: вызывается перед каждой функцией - пофиксить
@pytest.fixture(scope="function")
async def fake_films(es_client) -> List[Movie]:
    films = FilmFactory.batch(10)
    pretty_films = get_pretty_fake_films(films)
    pretty_elastic_films = get_fake_elastic_films(pretty_films)
    response = await load_fake_films(es_client, pretty_elastic_films)
    if response["errors"]:
        raise ConnectionError(f"Errors occurred during uploading fake films to ES index '{MOVIES_INDEX_NAME}'")
    return films


@pytest.fixture(scope="function")
async def fake_film(fake_films: List[Movie]) -> Movie:
    return fake_films[0]
