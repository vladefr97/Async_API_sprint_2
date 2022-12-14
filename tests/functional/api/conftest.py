from typing import List, Optional

import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from functional.api.settings import ES_HOST, MOVIES_INDEX_NAME, PERSON_INDEX_NAME
from functional.api.utils import check_es_indexes_exists, load_fake_films, load_fake_genres, load_fake_persons
from functional.factories.films import FakeFilm, FilmFactory, get_fake_elastic_films, get_pretty_fake_films
from functional.factories.genres import FakeGenre, GenreFactory, make_pretty_fake_genres
from functional.factories.persons import FakePerson, PersonFactory, make_pretty_fake_persons
from multidict import CIMultiDictProxy


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
def event_loop():
    yield asyncio.get_event_loop()


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
async def fake_films(es_client) -> List[FakeFilm]:
    films = FilmFactory.batch(10)
    pretty_films = get_pretty_fake_films(films)
    pretty_elastic_films = get_fake_elastic_films(pretty_films)
    response = await load_fake_films(es_client, pretty_elastic_films)
    if response["errors"]:
        raise ConnectionError(f"Errors occurred during uploading fake films to ES index '{MOVIES_INDEX_NAME}'")
    return pretty_films


@pytest.fixture(scope="session")
async def fake_genres(es_client) -> List[FakeGenre]:
    genres = GenreFactory.batch(10)
    pretty_genres = make_pretty_fake_genres(genres)
    response = await load_fake_genres(es_client, pretty_genres)
    if response["errors"]:
        raise ConnectionError(f"Errors occurred during uploading fake genres to ES index '{MOVIES_INDEX_NAME}'")
    return pretty_genres


@pytest.fixture(scope="session")
async def fake_persons(es_client) -> List[FakePerson]:
    persons = PersonFactory.batch(10)
    pretty_persons = make_pretty_fake_persons(persons)
    response = await load_fake_persons(es_client, pretty_persons)
    if response["errors"]:
        raise ConnectionError(f"Errors occurred during uploading fake persoons to ES index '{PERSON_INDEX_NAME}'")
    return pretty_persons


@pytest.fixture(scope="session")
async def fake_film(fake_films: List[FakeFilm]) -> FakeFilm:
    return fake_films[0]


@pytest.fixture(scope="session")
async def fake_genre(fake_genres: List[FakeGenre]) -> FakeGenre:
    return fake_genres[0]


@pytest.fixture(scope="session")
async def fake_person(fake_persons: List[FakePerson]) -> FakePerson:
    return fake_persons[0]
