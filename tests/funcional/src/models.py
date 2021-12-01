import datetime
from typing import Optional

from pydantic import BaseModel


class TestSet(BaseModel):
    film_id: str = '317df96f-2cbc-48fd-98ba-16a94cac68a0'
    person_id: str = '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1'
    genre_id: str = '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'
    film_search_phrase: str = 'Star Wars'
    person_search_phrase: str = 'ford'
    wrong_id: str = 'f0f0f0f-f0f0-f0f0-f0f0-f0f0f0f0f0f0'


test_set = TestSet()


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
