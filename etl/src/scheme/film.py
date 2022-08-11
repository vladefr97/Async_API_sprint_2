from typing import List, Optional

from pydantic import BaseModel, Field, validator


class PersonData(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: str
    imdb_rating: Optional[float] = Field(alias="rating")
    genre: Optional[List]
    title: str
    description: Optional[str]
    director: Optional[List]
    actors_names: Optional[List]
    writers_names: Optional[List]
    actors: Optional[List[PersonData]]
    writers: Optional[List[PersonData]]

    def _get_value_or_empty(cls, value, default_value):
        return value if value else default_value

    @validator("imdb_rating")
    def _set_float(cls, value) -> float:
        return cls._get_value_or_empty(value, float(0))

    @validator("description")
    def _set_str(cls, value) -> str:
        return cls._get_value_or_empty(value, "")

    @validator("genre", "director", "actors_names", "writers_names", "actors", "writers")
    def _set_list(cls, value) -> List:
        return cls._get_value_or_empty(value, [])
