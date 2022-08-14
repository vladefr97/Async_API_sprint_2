from fastapi import Query
from pydantic import BaseModel, Field


class ApiPaginator(BaseModel):
    page_number: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, default=10)


def get_paginator(
    page_number: int = Query(default=1, alias="filter[page]", ge=1),
    page_size: int = Query(default=10, alias="filter[size]", ge=1),
):
    return ApiPaginator(page_number=page_number, page_size=page_size)
