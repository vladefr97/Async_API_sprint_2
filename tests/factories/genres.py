from typing import List

from faker import Faker
from pydantic_factories import ModelFactory

from models.entities.genre import Genre

fake = Faker()


class FakeGenre(Genre):
    pass


class ElasticFakeGenre(Genre):
    pass


class GenreFactory(ModelFactory):
    __model__ = FakeGenre


def make_pretty_fake_genres(fake_genres: List[FakeGenre]):
    for genre in fake_genres:
        genre.name = fake.word()
    return fake_genres
