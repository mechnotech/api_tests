from pydantic import BaseSettings


class ShortFilmStructure(BaseSettings):
    id: str
    title: str
    imdb_rating: float


class FilmStructure(ShortFilmStructure):
    description: str
    genre: list
    actors: list
    writers: list
    directors: list
