from typing import Optional

import uuid

from pydantic import BaseModel

from models.mixins import ConfigMixin


class Genre(BaseModel, ConfigMixin):
    id: uuid.UUID
    name: str
    description: Optional[str]
