from pydantic_factories import ModelFactory

from models.entities.movie import Movie
from models.entities.actor import Actor
from models.entities.writer import Writer
from typing import List, Optional
from faker import Faker

fake = Faker()


class FakeFilm(Movie):
    pass


class ElasticFakeFilm(Movie):
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]


# TODO: переименовать в FakeFilmFactory
class FilmFactory(ModelFactory):
    __model__ = FakeFilm


def get_pretty_fake_films(fake_films: List[Movie]):
    for film in fake_films:
        film.title = fake.word()
        film.actors = list(map(lambda a: Actor(id=a.id, name=fake.name()), film.actors))
        film.directors = list(map(lambda d: fake.name(), film.directors))
        film.writers = list(map(lambda w: Writer(id=w.id, name=fake.name()), film.writers))
        film.genres = list(map(lambda g: fake.word(), film.genres))
    return fake_films


def get_fake_elastic_films(fake_films: List[FakeFilm]) -> List[ElasticFakeFilm]:
    elastic_films: List[ElasticFakeFilm] = []
    for film in fake_films:
        es_film = ElasticFakeFilm(**film.dict())
        es_film.actors_names = list(map(lambda a: a.name, film.actors))
        es_film.writers_names = list(map(lambda w: w.name, film.writers))
        elastic_films.append(es_film)
    return elastic_films
