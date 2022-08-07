from pydantic_factories import ModelFactory

from models.entities.movie import Movie


class FilmFactory(ModelFactory):
    __model__ = Movie
