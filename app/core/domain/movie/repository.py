from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.selectable import Select
from sqlalchemy import func, select, distinct, literal
import datetime as dt
from app.storages.pg.models import (
    film_work,
    person_film_work,
    person,
    genre_film_work,
    genre,
)


class GetUpdatedFilmsQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def _select_film_works(cls):
        cls.__result_query = select(
            film_work.c.id,
            film_work.c.title,
            film_work.c.description,
            film_work.c.rating.label("imdb_rating"),
            func.coalesce(func.array_agg(distinct(genre.c.name)), literal("{}")).label(
                "genres"
            ),
            func.coalesce(
                func.array_agg(distinct(person.c.full_name)).filter(
                    (person.c.id.is_not(None)) & (person_film_work.c.role == "director")
                ),
                literal("{}"),
            ).label("directors_names"),
            func.coalesce(
                func.array_agg(distinct(person.c.full_name)).filter(
                    (person.c.id.is_not(None)) & (person_film_work.c.role == "actor")
                ),
                literal("{}"),
            ).label("actors_names"),
            func.coalesce(
                func.array_agg(distinct(person.c.full_name)).filter(
                    (person.c.id.is_not(None)) & (person_film_work.c.role == "writer")
                ),
                literal("{}"),
            ).label("writers_names"),
            func.coalesce(
                func.json_agg(
                    distinct(
                        func.jsonb_build_object(
                            "id", person.c.id, "name", person.c.full_name
                        )
                    )
                ).filter(person_film_work.c.role == "director"),
                literal([], type_=JSON),
            ).label("directors"),
            func.coalesce(
                func.json_agg(
                    distinct(
                        func.jsonb_build_object(
                            "id", person.c.id, "name", person.c.full_name
                        )
                    )
                ).filter(person_film_work.c.role == "actor"),
                literal([], type_=JSON),
            ).label("actors"),
            func.coalesce(
                func.json_agg(
                    distinct(
                        func.jsonb_build_object(
                            "id", person.c.id, "name", person.c.full_name
                        )
                    )
                ).filter(person_film_work.c.role == "writer"),
                literal([], type_=JSON),
            ).label("writers"),
            func.greatest(
                func.max(film_work.c.modified),
                func.max(person_film_work.c.created),
                func.max(person.c.modified),
                func.max(genre_film_work.c.created),
                func.max(genre.c.modified),
            ).label("last_change_date"),
        )
        return cls

    @classmethod
    def _join_related(cls):
        cls.__result_query = (
            cls.__result_query.outerjoin(
                person_film_work, person_film_work.c.film_work_id == film_work.c.id
            )
            .outerjoin(person, person.c.id == person_film_work.c.person_id)
            .outerjoin(
                genre_film_work, genre_film_work.c.film_work_id == film_work.c.id
            )
            .outerjoin(genre, genre.c.id == genre_film_work.c.genre_id)
        )
        return cls

    @classmethod
    def _group_by(cls):
        cls.__result_query = cls.__result_query.group_by(film_work.c.id)
        return cls

    @classmethod
    def _having_after(cls, after: dt.datetime):
        cls.__result_query = cls.__result_query.having(
            func.greatest(
                func.max(film_work.c.modified),
                func.max(person_film_work.c.created),
                func.max(person.c.modified),
                func.max(genre_film_work.c.created),
                func.max(genre.c.modified),
            )
            > literal(after)
        )
        return cls

    @classmethod
    def _order_by(cls):
        cls.__result_query = cls.__result_query.order_by(film_work.c.modified)
        return cls

    @classmethod
    def _build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, after: dt.datetime) -> Select:
        return (
            cls._select_film_works()
            ._join_related()
            ._group_by()
            ._having_after(after=after)
            ._order_by()
            ._build()
        )
