from typing import Optional

import uuid

from pydantic import BaseModel


class GenreSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
