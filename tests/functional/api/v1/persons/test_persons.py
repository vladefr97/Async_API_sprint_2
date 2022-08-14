from http import HTTPStatus

import pytest

from functional.factories.persons import FakePerson
from functional.models.entities.movie import Movie
from functional.api.settings import FILMS_V1_URL, PERSONS_V1_URL
from functional.api.types import AsyncGET


class TestPersons:
    @pytest.mark.asyncio
    async def test_persons_response_size(self, make_get_request: AsyncGET):
        RESPONSE_SIZE = 5
        query_param = {"filter[size]": RESPONSE_SIZE}
        response = await make_get_request(PERSONS_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == RESPONSE_SIZE