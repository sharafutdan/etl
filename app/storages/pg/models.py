from sqlalchemy import Table

from app.storages.pg.base import engine, metadata

film_work = Table("film_work", metadata, autoload_with=engine)
person_film_work = Table("person_film_work", metadata, autoload_with=engine)
person = Table("person", metadata, schema="content", autoload_with=engine)
genre_film_work = Table(
    "genre_film_work", metadata, schema="content", autoload_with=engine
)
genre = Table("genre", metadata, schema="content", autoload_with=engine)
