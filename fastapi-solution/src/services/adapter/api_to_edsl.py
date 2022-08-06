from typing import List, Optional

from api.filters import ApiQueryFilters
from api.sorting import ApiSortOption


class API2EDSLQueryAdapter:
    def get_edsl_from_api(self, query_filters: ApiQueryFilters, sort_options: Optional[List[ApiSortOption]]) -> dict:
        pass
