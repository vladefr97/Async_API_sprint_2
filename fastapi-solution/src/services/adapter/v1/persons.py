from typing import Any, Dict, List, Optional

from functools import lru_cache

from api.pagination import ApiPaginator
from api.sorting import ApiSortOption
from api.v1.filters.persons import PersonsAPIQueryFilters
from services.adapter.api_to_edsl import API2EDSLQueryAdapter


class PersonsAPI2EDSLQueryAdapter(API2EDSLQueryAdapter):
    __edsl_query: Dict[str, Any] = {}

    def get_edsl_from_api(  # pylint: disable=arguments-differ
        self, query_filters: PersonsAPIQueryFilters, paginator: ApiPaginator
    ) -> Dict[str, Any]:
        self.__refresh_edsl_query()
        self.__set_page(paginator.page_number)
        self.__set_size(paginator.page_size)
        if query_filters.names:
            self.__set_names_filter(query_filters.names)
        else:
            self.__edsl_query.pop("query")
        return self.__edsl_query

    def __set_page(self, page: int) -> None:
        self.__edsl_query["from"] = page

    def __set_size(self, size: int) -> None:
        self.__edsl_query["size"] = size

    def __set_names_filter(self, names: List[str]) -> None:
        self.__edsl_query["query"]["bool"]["filter"].append({"match": {"name": " ".join(names)}})

    def __refresh_edsl_query(self) -> None:
        self.__edsl_query = {
            "from": 0,
            "size": 0,
            "query": {
                "bool": {
                    "filter": [],
                }
            },
        }


@lru_cache()
def get_api_to_edsl_adapter() -> PersonsAPI2EDSLQueryAdapter:
    return PersonsAPI2EDSLQueryAdapter()
