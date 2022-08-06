from typing import List, Optional

from pydantic import root_validator

from api.filters import ApiQueryFilters


class FilmsAPIQueryFilters(ApiQueryFilters):
    imdb_rating_lt: Optional[float]
    imdb_rating_gt: Optional[float]
    in_genres: Optional[List[str]]
    in_actors: Optional[List[str]]
    in_writers: Optional[List[str]]
    in_directors: Optional[List[str]]

    # Проверяем соответствие параметров imdb_rating_lt и imdb_rating_gt
    @classmethod
    @root_validator
    def check_imdb_rating_filters_match(cls, values):
        imdb_rating_lt, imdb_rating_gt = values.get("imdb_rating_lt"), values.get("imdb_rating_gt")
        if imdb_rating_gt and imdb_rating_gt and imdb_rating_lt < imdb_rating_gt:
            raise ValueError("filter imdb_rating_lt should be less than imdb_rating_gt")
        return values


class FilmsApiQuerySorting:
    imdb_rating_desc = ""
