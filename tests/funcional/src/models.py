import datetime
from typing import Optional

from pydantic import BaseModel


class APIModel(BaseModel):
    id: str


class ShortFilm(APIModel):
    title: str
    imdb_rating: float


class Film(ShortFilm):
    description: str
    genre: list
    actors: list
    writers: list
    directors: list


class ShortGenre(APIModel):
    name: str
    description: Optional[str]


class Genre(ShortGenre):
    score: int


class ShortPerson(APIModel):
    full_name: str
    birthday: Optional[datetime.date]


class Person(ShortPerson):
    role: Optional[dict]
