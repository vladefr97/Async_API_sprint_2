from pydantic import BaseModel, Field


class Person(BaseModel):
    id: str
    name: str = Field(alias="full_name")
