
from http import HTTPStatus

import pytest
from functional.api.settings import FILMS_V1_URL, PERSONS_V1_URL
from functional.api.types import AsyncGET
from functional.factories.persons import FakePerson


class TestPerson:
    @pytest.mark.asyncio
    async def test_search_detailed(self, make_get_request: AsyncGET, fake_person: FakePerson):
        response = await make_get_request(PERSONS_V1_URL + str(fake_person.id))
        assert response.status == HTTPStatus.OK
        assert response.body["id"] == str(fake_person.id)

    @pytest.mark.asyncio
    async def test_search_detailed_with_bad_id(self, make_get_request: AsyncGET, fake_person: FakePerson):
        response = await make_get_request(FILMS_V1_URL + str(fake_person.id) + "bad")
        assert response.status == HTTPStatus.NOT_FOUND
