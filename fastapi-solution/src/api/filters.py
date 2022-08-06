from typing import Optional

from pydantic import BaseModel


# TODO: сделать дефолтное значение для этих параметров только в одном месте (сейчас во многих дублируется)
class ApiQueryFilters(BaseModel):
    page: Optional[int] = 1
    size: Optional[int] = 10
