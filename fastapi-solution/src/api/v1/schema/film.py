from typing import List, Optional

import uuid
from datetime import datetime

# Используем pydantic для упрощения работы при перегонке данных из json в объекты
from pydantic import BaseModel


class NestedPersonSchema(BaseModel):
    id: uuid.UUID
    name: str


class FilmSchema(BaseModel):
    id: uuid.UUID
    title: str
    imdb_rating: float
    description: Optional[str] = ""
    creation_date: Optional[datetime]
    # TODO: уточнять поля словаря или поменять на nested модели
    actors: List[NestedPersonSchema] = []
    director: List[NestedPersonSchema] = []
    writers: List[NestedPersonSchema] = []
    genres: List[str]
