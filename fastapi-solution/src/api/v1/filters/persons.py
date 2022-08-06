from typing import List, Optional

from api.filters import ApiQueryFilters


class PersonsAPIQueryFilters(ApiQueryFilters):
    names: Optional[List[str]]
