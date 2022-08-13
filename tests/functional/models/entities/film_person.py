import uuid

from pydantic import BaseModel

from models.mixins import ConfigMixin


class FilmPerson(BaseModel, ConfigMixin):
    id: uuid.UUID
    name: str
