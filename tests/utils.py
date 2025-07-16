import datetime as dt

from app.core.domain.movie.dto import FilmWorkDTO
from tests.factory.movie import FilmWorkFactory


def films(created_at: dt.datetime, updated_at: dt.datetime) -> list[FilmWorkDTO]:
    return [
        *[
            f
            for f in FilmWorkFactory.batch(
                size=10,
                creation_date=created_at,
                modified=updated_at,
            )
        ],
        *[
            f
            for f in FilmWorkFactory.batch(
                size=10,
                creation_date=created_at - dt.timedelta(days=5),
                modified=updated_at - dt.timedelta(days=5),
            )
        ],
    ]
