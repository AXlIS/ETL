from abc import abstractmethod

import psycopg2
from backoff import backoff
from es_data import MovieData, PersonData, GenreData
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from queries import (LOAD_FILMS_DATA_QUERY, LOAD_FILMS_ID_ONLY,
                     LOAD_FILMS_ID_QUERY_BY_PERSONS, LOAD_PERSONS_ID_QUERY,
                     LOAD_GENRES_ID_QUERY, LOAD_FILMS_ID_QUERY_BY_GENRES,
                     LOAD_GENRE_DATA_QUERY, LOAD_PERSON_DATA_QUERY,
                     LOAD_PERSONS_ID_QUERY_BY_ROLE)
from state import JsonFileStorage, State


class PostgresLoader:
    dataclass = None

    def __init__(self, config, state_key):
        self.config = config
        self.offset = 0
        self.limit = 100
        self.data = []
        self.time = State(JsonFileStorage('volumes/etl_state.json')).get_state(state_key)

    def get_connection(self) -> _connection:
        """Соединение с базой данных"""
        with psycopg2.connect(
                **self.config,
                cursor_factory=DictCursor
        ) as pg_conn:
            return pg_conn

    @backoff()
    def load_data(self, query) -> None:
        """Получение данных о film_works"""
        cursor = self.get_connection().cursor()
        while True:
            cursor.execute(query())
            items = cursor.fetchall()
            if not items:
                break
            for item in items:
                item_dict = dict(item)
                self.data.append(self.dataclass(**item_dict).dict())
            self.offset += self.limit
        cursor.close()
        self.offset = 0

    def load_id(self, query) -> str:
        """Запрос на получение id с обновленными данными в зависимости от источника"""
        if not self.time:
            return query
        index = query.rfind('ORDER BY id')
        return f"{query[:index]} WHERE modified > '{self.time}' {query[index:]}"

    @abstractmethod
    def load(self) -> list:
        """Сохранение данных, в зависимости от источника"""
        pass


class MovieOnlyLoader(PostgresLoader):
    dataclass = MovieData

    def load_films_by_id_only(self) -> str:
        """Запрос на получение id film_works, информация о которых была обновлена"""
        return LOAD_FILMS_DATA_QUERY % (self.load_id(LOAD_FILMS_ID_ONLY), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_films_by_id_only)
        return self.data


class MoviesByPersonLoader(PostgresLoader):
    dataclass = MovieData

    def load_films_id_by_persons(self) -> str:
        """Запрос на получение id film_works, в которых участвовали люди с обновленной информацией"""
        return LOAD_FILMS_ID_QUERY_BY_PERSONS % self.load_id(LOAD_PERSONS_ID_QUERY)

    def load_films_by_persons(self) -> str:
        """Запрос на получение всех данных о фильмах, в которых участвовали люди с обновленной информацией"""
        return LOAD_FILMS_DATA_QUERY % (self.load_films_id_by_persons(), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_films_by_persons)
        return self.data


class MoviesByGenreLoader(PostgresLoader):
    dataclass = MovieData

    def load_films_id_by_genre(self) -> str:
        """Запрос на получение id film_works, в которых есть жанры с обновленной информацией"""
        return LOAD_FILMS_ID_QUERY_BY_GENRES % self.load_id(LOAD_GENRES_ID_QUERY)

    def load_films_by_genre(self) -> str:
        """Запрос на получение всех данных о фильмах, в которых есть жанры с обновленной информацией"""
        return LOAD_FILMS_DATA_QUERY % (self.load_films_id_by_genre(), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_films_by_genre)
        return self.data


class GenreLoader(PostgresLoader):
    dataclass = GenreData

    def load_genres_by_id_only(self):
        """Запрос на получение id genre, информация о которых была обновлена"""
        return LOAD_GENRE_DATA_QUERY % (self.load_id(LOAD_GENRES_ID_QUERY), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_genres_by_id_only)
        return self.data


class PersonOnlyLoader(PostgresLoader):
    dataclass = PersonData

    def load_persons_by_id_only(self):
        """Запрос на получение id person, информация о которых была обновлена"""
        return LOAD_PERSON_DATA_QUERY % (self.load_id(LOAD_PERSONS_ID_QUERY), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_persons_by_id_only)
        return self.data


class PersonByRoleLoader(PostgresLoader):
    dataclass = PersonData

    def load_persons_id_by_role(self):
        """Запрос на получение id person"""
        return LOAD_PERSON_DATA_QUERY % (self.load_id(LOAD_PERSONS_ID_QUERY_BY_ROLE), self.limit, self.offset)

    def load(self) -> list:
        self.load_data(self.load_persons_id_by_role)
        return self.data
