from typing import List, Optional

import uuid

from pydantic import BaseModel, Field

from models.entities.actor import Actor
from models.entities.writer import Writer
from models.mixins import ConfigMixin


# TODO: есть вариант сделать одну модель без наследованием с полем type = Movie | Series
class FilmWork(BaseModel, ConfigMixin):
    id: uuid.UUID
    title: str
    imdb_rating: float = Field(le=10, ge=0)
    description: Optional[str]
    # creation_date: Optional[datetime]
    actors: List[Actor] = []
    # TODO: нужно дополнить индекс movies, чтобы был List[Director], но по заданию в индексе массив строк
    directors: List[str] = Field(alias="director")
    writers: List[Writer] = []
    # TODO: Тут должен быть объект Genre, для простоты пока что сделана строка
    genres: List[str] = Field(alias="genre")

    class Config:
        allow_population_by_field_name = True
