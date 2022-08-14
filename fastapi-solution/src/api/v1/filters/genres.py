from api.filters import ApiQueryFilters


class GenresAPIQueryFilters(ApiQueryFilters):
    page: int
    size: int
