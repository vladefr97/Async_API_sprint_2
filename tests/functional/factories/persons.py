from typing import List

from faker import Faker
from functional.models.entities.film_person import FilmPerson
from pydantic_factories import ModelFactory

fake = Faker()


class FakePerson(FilmPerson):
    pass


class ElasticFakePerson(FilmPerson):
    pass


class PersonFactory(ModelFactory):
    __model__ = FakePerson


def make_pretty_fake_persons(fake_persons: List[FakePerson]):
    for person in fake_persons:
        person.name = fake.word()
    return fake_persons
