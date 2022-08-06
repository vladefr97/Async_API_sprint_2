import uuid

from pydantic import BaseModel


class PersonSchema(BaseModel):
    id: uuid.UUID
    name: str
