from typing import Any, Dict, List, Optional

from enum import Enum
from functools import lru_cache

from pydantic import BaseModel

from api.pagination import ApiPaginator
from api.v1.filters.films import FilmsAPIQueryFilters
from api.v1.sorting.films import FilmsApiSortOption
from services.adapter.api_to_edsl import API2EDSLQueryAdapter


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"


class EDSLSort(BaseModel):
    sort_field: str
    order: SortOrder


sortOptionToEDSLDict: Dict[FilmsApiSortOption, EDSLSort] = {
    FilmsApiSortOption.IMDB_RATING_ASC: EDSLSort(sort_field="imdb_rating", order=SortOrder.ASC),
    FilmsApiSortOption.IMDB_RATING_DESC: EDSLSort(sort_field="imdb_rating", order=SortOrder.DESC),
}


class FilmsAPI2EDSLQueryAdapter(API2EDSLQueryAdapter):
    __edsl_query: Dict[str, Any] = {}

    def __init__(self):
        self.__set_query_filters(
            FilmsAPIQueryFilters(),
        )
        self.__refresh_edsl_query()

    def get_edsl_from_api(
        self, query_filters: FilmsAPIQueryFilters, sort_options: List[FilmsApiSortOption], paginator: ApiPaginator
    ) -> dict:
        self.__set_query_filters(query_filters)
        self.__refresh_edsl_query()
        self.__set_edsl_filters()
        self.__set_edsl_sort_options(sort_options)
        self.__set_page(paginator.page_number)
        self.__set_size(paginator.page_size)
        return self.__edsl_query

    def __set_query_filters(self, api_filters):
        self.__query_filters = api_filters

    def __refresh_edsl_query(self):
        self.__edsl_query = {
            "from": 0,
            "size": 0,
            "sort": {"imdb_rating": "desc"},
            "query": {
                "bool": {
                    "filter": [],
                }
            },
        }

    def __set_edsl_sort_options(self, sort_options: List[FilmsApiSortOption]) -> None:
        for option in sort_options:
            self.__append_to_edsl_sort(sortOptionToEDSLDict[option])

    def __set_edsl_filters(self):
        self.__set_rating_edsl_filter()
        self.__set_genres_edsl_filter()
        self.__set_actors_edsl_filter()
        self.__set_directors_edsl_filter()
        self.__set_writers_edsl_filter()

    def __set_page(self, page_number: int) -> None:
        self.__edsl_query["from"] = page_number

    def __set_size(self, page_size: int) -> None:
        self.__edsl_query["size"] = page_size

    def __append_to_edsl_sort(self, sort: EDSLSort) -> None:
        self.__edsl_query["sort"][sort.sort_field] = sort.order.value

    def __append_to_edsl_bool_filters(self, query_filter: dict) -> None:
        self.__edsl_query["query"]["bool"]["filter"].append(query_filter)

    def __set_actors_edsl_filter(self) -> None:
        if self.__query_filters.in_actors:
            self.__append_to_edsl_bool_filters({"match": {"actors_names": " ".join(self.__query_filters.in_actors)}})

    def __set_writers_edsl_filter(self) -> None:
        if self.__query_filters.in_writers:
            self.__append_to_edsl_bool_filters({"match": {"writers_names": " ".join(self.__query_filters.in_writers)}})

    def __set_directors_edsl_filter(self) -> None:
        if self.__query_filters.in_directors:
            self.__append_to_edsl_bool_filters({"match": {"director": " ".join(self.__query_filters.in_directors)}})

    def __set_rating_edsl_filter(self) -> None:
        rating_filter = {}
        if self.__query_filters.imdb_rating_gt:
            rating_filter["gt"] = self.__query_filters.imdb_rating_gt
        if self.__query_filters.imdb_rating_lt:
            rating_filter["lt"] = self.__query_filters.imdb_rating_lt
        if rating_filter:
            self.__append_to_edsl_bool_filters({"range": {"imdb_rating": rating_filter}})

    def __set_genres_edsl_filter(self) -> None:
        if self.__query_filters.in_genres:
            self.__append_to_edsl_bool_filters({"terms": {"genre": self.__query_filters.in_genres}})


@lru_cache()
def get_api_to_edsl_adapter() -> FilmsAPI2EDSLQueryAdapter:
    return FilmsAPI2EDSLQueryAdapter()
