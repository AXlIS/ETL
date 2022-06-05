from postgres_loader import (MovieOnlyLoader, MoviesByPersonLoader,
                             MoviesByGenreLoader, GenreLoader,
                             PersonOnlyLoader, PersonByRoleLoader)

tasks = [
    {
        "class_loader": MovieOnlyLoader,
        "state_key": "movie_only_update",
        "index_name": "movies",
        "schema": "schemas/movies.json",
    },
    {
        "class_loader": MoviesByPersonLoader,
        "state_key": "movie_by_person_update",
        "index_name": "movies",
        "schema": "schemas/movies.json",
    },
    {
        "class_loader": MoviesByGenreLoader,
        "state_key": "movie_by_genre_update",
        "index_name": "movies",
        "schema": "schemas/movies.json",
    },
    {
        "class_loader": GenreLoader,
        "state_key": "genre_only_update",
        "index_name": "genres",
        "schema": "schemas/genres.json",
    },
    {
        "class_loader": PersonOnlyLoader,
        "state_key": "person_only_update",
        "index_name": "persons",
        "schema": "schemas/persons.json",
    },
    {
        "class_loader": PersonByRoleLoader,
        "state_key": "person_by_role_update",
        "index_name": "persons",
        "schema": "schemas/persons.json",
    },
]
