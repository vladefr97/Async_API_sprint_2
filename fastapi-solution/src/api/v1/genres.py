from typing import List

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.filters import GenresAPIQueryFilters
from api.v1.messages.eng import GENRE_NOT_FOUND_MSG, GENRES_NOT_FOUND_MSG
from api.v1.schema import GenreSchema
from models.entities.genre import Genre
from services.adapter.v1.genres import GenresAPI2EDSLQueryAdapter, get_api_to_edsl_adapter
from services.request.genre import GenreService, get_genre_service
from services.request.genres import GenresRequestService, get_genres_service

router = APIRouter()


def get_query_filters(
    page: int = Query(default=1, alias="filter[page]", ge=1), size: int = Query(default=10, alias="filter[size]", ge=1)
) -> GenresAPIQueryFilters:
    return GenresAPIQueryFilters(page=page, size=size)


def to_genre_api_schema(genre: Genre) -> GenreSchema:
    return GenreSchema(**genre.dict())


@router.get(
    "/",
    response_model=List[GenreSchema],
    summary="List of genres",
    description="Get list of genres filtered by query params",
)
async def genres_list(
    genres_service: GenresRequestService = Depends(get_genres_service),
    filters: GenresAPIQueryFilters = Depends(get_query_filters),
    adapter: GenresAPI2EDSLQueryAdapter = Depends(get_api_to_edsl_adapter),
) -> List[GenreSchema]:
    dsl = adapter.get_edsl_from_api(filters)
    genres = await genres_service.get_genres(edsl_query=dsl)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRES_NOT_FOUND_MSG)
    return [to_genre_api_schema(genre) for genre in genres]


@router.get(
    "/{genre_id}",
    response_model=GenreSchema,
    summary="Information about one film",
    description="Get information about one genre with specified UUID",
)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreSchema:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=GENRE_NOT_FOUND_MSG)
    return to_genre_api_schema(genre)
