from typing import List

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from api.pagination import ApiPaginator, get_paginator
from api.v1.filters import FilmsAPIQueryFilters
from api.v1.messages.eng import FILM_NOT_FOUND_MSG, FILMS_NOT_FOUND_MSG
from api.v1.schema import FilmSchema
from api.v1.sorting import FilmsApiSortOption
from models.entities.movie import Movie
from services.adapter.v1.films import FilmsAPI2EDSLQueryAdapter, get_api_to_edsl_adapter
from services.request.film import FilmService, get_film_service
from services.request.films import FilmsRequestService, get_films_service

router = APIRouter()


# TODO: поискать решение, чтобы можно было указывать параметры не в функции, а в отдельной модели
def get_query_filters(
    imdb_rating_lt: float = Query(default=None, le=10, ge=0, alias="filter[imdb_rating_lt]"),
    imdb_rating_gt: float = Query(default=None, le=10, ge=0, alias="filter[imdb_rating_gt]"),
    in_genres: List[str] = Query(default=[], alias="filter[in_genres]"),
    in_actors: List[str] = Query(default=[], alias="filter[in_actors]"),
    in_writers: List[str] = Query(default=[], alias="filter[in_writers]"),
    in_directors: List[str] = Query(default=[], alias="filter[in_directors]"),
) -> FilmsAPIQueryFilters:
    try:
        return FilmsAPIQueryFilters(
            imdb_rating_lt=imdb_rating_lt,
            imdb_rating_gt=imdb_rating_gt,
            in_genres=in_genres,
            in_actors=in_actors,
            in_writers=in_writers,
            in_directors=in_directors,
        )
    except ValueError as err:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(err)) from err


def to_film_api_schema(movie: Movie) -> FilmSchema:
    return FilmSchema(**movie.dict())


@router.get(
    "/",
    response_model=List[FilmSchema],
    summary="List of films",
    description="Get list of films filtered by query params",
)
async def films_list(  # pylint: disable=too-many-arguments
    films_service: FilmsRequestService = Depends(get_films_service),
    filters: FilmsAPIQueryFilters = Depends(get_query_filters),
    paginator: ApiPaginator = Depends(get_paginator),
    sort_options: List[FilmsApiSortOption] = Query(default=[], alias="sort"),
    adapter: FilmsAPI2EDSLQueryAdapter = Depends(get_api_to_edsl_adapter),
) -> List[FilmSchema]:
    print(paginator)
    dsl = adapter.get_edsl_from_api(filters, sort_options, paginator)
    films = await films_service.get_films(edsl_query=dsl)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILMS_NOT_FOUND_MSG)
    return [to_film_api_schema(film) for film in films]


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/{film_id}",
    response_model=FilmSchema,
    summary="Information about one film",
    description="Get information about one film with specified UUID",
)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmSchema:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND_MSG)
    return to_film_api_schema(film)
