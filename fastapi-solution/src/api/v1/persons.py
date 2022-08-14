from typing import List

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query

from api.pagination import ApiPaginator, get_paginator
from api.v1.filters import PersonsAPIQueryFilters
from api.v1.messages.eng import PERSON_NOT_FOUND_MSG
from api.v1.schema import PersonSchema
from models.entities.film_person import FilmPerson
from services.adapter.v1.persons import PersonsAPI2EDSLQueryAdapter, get_api_to_edsl_adapter
from services.request.person import PersonService, get_person_service
from services.request.persons import PersonsRequestService, get_persons_service

router = APIRouter()


def get_query_filters(
    names: List[str] = Query(default=[], alias="filter[names]"),
    page: int = Query(default=1, alias="filter[page]", ge=1),
    size: int = Query(default=10, alias="filter[size]", ge=1),
) -> PersonsAPIQueryFilters:
    return PersonsAPIQueryFilters(names=names, page=page, size=size)


def to_person_api_schema(film_person: FilmPerson) -> PersonSchema:
    return PersonSchema(**film_person.dict())


@router.get(
    "/",
    response_model=List[PersonSchema],
    summary="List of persons",
    description="Get list of persons filtered by query params",
)
async def persons_list(
    persons_service: PersonsRequestService = Depends(get_persons_service),
    filters: PersonsAPIQueryFilters = Depends(get_query_filters),
    paginator: ApiPaginator = Depends(get_paginator),
    adapter: PersonsAPI2EDSLQueryAdapter = Depends(get_api_to_edsl_adapter),
) -> List[PersonSchema]:
    dsl = adapter.get_edsl_from_api(query_filters=filters, paginator=paginator)
    persons = await persons_service.get_persons(edsl_query=dsl)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND_MSG)
    return [to_person_api_schema(person) for person in persons]


@router.get(
    "/{person_id}",
    response_model=PersonSchema,
    summary="Information about one person",
    description="Get information about one person with specified UUID",
)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonSchema:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PERSON_NOT_FOUND_MSG)
    return to_person_api_schema(person)
