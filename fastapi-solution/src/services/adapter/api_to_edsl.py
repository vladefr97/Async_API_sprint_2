from typing import List, Optional

from api.filters import ApiQueryFilters
from api.pagination import ApiPaginator
from api.sorting import ApiSortOption


class API2EDSLQueryAdapter:
    def get_edsl_from_api(
        self,
        query_filters: Optional[ApiQueryFilters],
        sort_options: Optional[List[ApiSortOption]],
        paginator: Optional[ApiPaginator],
    ) -> dict:
        ...
