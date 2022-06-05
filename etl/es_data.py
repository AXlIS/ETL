from typing import Dict, List, Optional, Union
from uuid import UUID
from datetime import date

from pydantic import BaseModel

OBJ_KEY = str
OBJ_VALUE = Optional[Union[float, str, UUID]]


class MovieData(BaseModel):
    id: Union[str, UUID]
    imdb_rating: Optional[float] = None
    genre: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    director: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
    actors_names: List[str] = None
    writers_names: List[str] = None
    actors: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
    writers: List[Dict[OBJ_KEY, OBJ_VALUE]] = None


class GenreData(BaseModel):
    id: Union[str, UUID]
    name: str
    description: Optional[str] = None


class PersonData(BaseModel):
    id: Union[str, UUID]
    full_name: str
    birth_date: date = None
    role: List[str] = None
    films: List[Dict[OBJ_KEY, OBJ_VALUE]] = None
