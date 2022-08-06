from typing import Any, Dict, List, Optional

from functools import lru_cache

from api.sorting import ApiSortOption
from api.v1.filters.genres import GenresAPIQueryFilters
from services.adapter.api_to_edsl import API2EDSLQueryAdapter


class GenresAPI2EDSLQueryAdapter(API2EDSLQueryAdapter):
    __edsl_query: Dict[str, Any] = {}

    def get_edsl_from_api(  # pylint: disable=arguments-differ
        self, query_filters: GenresAPIQueryFilters, sort_options: Optional[List[ApiSortOption]] = None
    ) -> Dict[str, Any]:
        self.__refresh_edsl_query()
        self.__set_page(query_filters.page)
        self.__set_size(query_filters.size)
        return self.__edsl_query

    def __set_page(self, page: int) -> None:
        self.__edsl_query["from"] = page

    def __set_size(self, size: int) -> None:
        self.__edsl_query["size"] = size

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
def get_api_to_edsl_adapter() -> GenresAPI2EDSLQueryAdapter:
    return GenresAPI2EDSLQueryAdapter()
