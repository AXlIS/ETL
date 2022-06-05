LOAD_PERSONS_ID_QUERY = """
    SELECT DISTINCT id
    FROM content.person
    ORDER BY id
"""

LOAD_PERSONS_ID_QUERY_BY_ROLE = """
    SELECT DISTINCT person_id as id
    FROM content.person_film_work
    ORDER BY id
"""

LOAD_GENRES_ID_QUERY = """
    SELECT DISTINCT id
    FROM content.genre
    ORDER BY id
"""

LOAD_FILMS_ID_QUERY_BY_GENRES = """
    SELECT distinct fw.id
    FROM content.film_work fw
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    WHERE gfw.genre_id IN (%s)
    GROUP BY fw.id
"""

LOAD_FILMS_ID_QUERY_BY_PERSONS = """
    SELECT distinct fw.id
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    WHERE pfw.person_id IN (%s)
    GROUP BY fw.id
"""

LOAD_FILMS_ID_ONLY = """
    SELECT DISTINCT id
    FROM content.film_work
    ORDER BY id
"""

LOAD_FILMS_DATA_QUERY = """
    SELECT fw.id,
       fw.title,
       ARRAY_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)) AS genre,
       ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers,
       ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'director') AS director,
       ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
       ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
       ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
       fw.description,
       fw.rating as imdb_rating,
       fw.modified,
       fw.type
    FROM content.film_work fw
    JOIN content.genre_film_work gfw ON fw.id = gfw.film_work_id
    JOIN content.genre g ON gfw.genre_id = g.id
    LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id
    LEFT JOIN content.person p ON pfw.person_id = p.id
    WHERE fw.id IN (%s)
    GROUP BY fw.id, fw.modified
    ORDER BY fw.modified
    LIMIT %s 
    OFFSET %s;
"""

LOAD_GENRE_DATA_QUERY = """
    SELECT id, name, description
    FROM content.genre
    WHERE id IN (%s)
    GROUP BY id, modified
    ORDER BY modified
    LIMIT %s 
    OFFSET %s;
"""

LOAD_PERSON_DATA_QUERY = """
    SELECT p.id,
       p.full_name,
       p.birth_date,
       array_agg(DISTINCT pfw.role) as role,
       array_agg(DISTINCT jsonb_build_object('id', fw.id, 'title', fw.title, 'imdb_rating', fw.rating, 'role', pfw.role))
 as films
    FROM content.person as p
    LEFT JOIN content.person_film_work pfw on p.id = pfw.person_id
    LEFT JOIN content.film_work fw on fw.id = pfw.film_work_id
    WHERE p.id IN (%s)
    GROUP BY p.id, p.modified
    ORDER BY p.modified
    LIMIT %s 
    OFFSET %s;
"""
