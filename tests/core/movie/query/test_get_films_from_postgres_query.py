import datetime as dt
from unittest.mock import patch
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from app.core.domain.movie.query import GetFilmsFromPostgresQuery
from app.storages.pg.models import film_work
from tests.utils import films


def test_get_films_from_pg_query_not_found_any_films(
    session: Session, get_films_from_postgres_query: GetFilmsFromPostgresQuery
) -> None:
    with patch.object(get_films_from_postgres_query, "_log", MagicMock()) as mock:
        movies = list(get_films_from_postgres_query.execute(value=dt.datetime.now()))
    assert not len(movies)
    assert not mock.called, f"Got {mock.called} calls, expected {not mock.called}"


def test_get_films_from_pg_query_filters_films(
    session: Session, get_films_from_postgres_query: GetFilmsFromPostgresQuery
) -> None:
    curr_time = dt.datetime.now(tz=dt.UTC)
    # найдем все фильмы, которые обновились на протяжении дня
    session.execute(
        statement=film_work.insert(),
        params=[f.as_dict for f in films(created_at=curr_time, updated_at=curr_time)],
    )
    last_sync_at = curr_time - dt.timedelta(days=1)
    with patch.object(get_films_from_postgres_query._log, "info", MagicMock()) as mock:
        movies = list(get_films_from_postgres_query.execute(value=last_sync_at))
    assert len(movies) == 10
    assert mock.call_count == 10
