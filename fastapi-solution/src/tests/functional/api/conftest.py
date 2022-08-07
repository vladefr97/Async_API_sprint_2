from typing import Optional

from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
from tests.factories.films import FilmFactory
from tests.functional.api.settings import ES_HOST, MOVIES_INDEX_NAME
from tests.functional.api.utils import check_es_indexes_exists, load_fake_films


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=ES_HOST)
    check_es_indexes_exists(client)
    yield client
    await client.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
async def fake_films(es_client):
    films = [FilmFactory.build() for i in range(10)]
    response = await load_fake_films(es_client, films)
    if response["errors"]:
        raise ConnectionError(f"Errors occurred during uploading fake films to ES index '{MOVIES_INDEX_NAME}'")
    return films
