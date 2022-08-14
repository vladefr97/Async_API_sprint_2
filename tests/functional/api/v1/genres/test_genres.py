from http import HTTPStatus

import pytest

from api.settings import GENRES_V1_URL
from api.types import AsyncGET


class TestGenres:
    @pytest.mark.asyncio
    async def test_genres_response_size(self, make_get_request: AsyncGET):
        RESPONSE_SIZE = 5
        query_param = {"filter[size]": RESPONSE_SIZE}
        response = await make_get_request(GENRES_V1_URL, query_param)
        assert response.status == HTTPStatus.OK
        assert len(response.body) == RESPONSE_SIZE
