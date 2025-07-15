from app.core.domain.movie.query import GetFilmsLastSyncTimeQuery
from unittest.mock import patch, MagicMock

from tests.tools import spy_decorator


def test_get_films_last_sync_time_query_success(
    get_films_last_sync_time_query: GetFilmsLastSyncTimeQuery,
) -> None:
    provider = get_films_last_sync_time_query._last_sync_time_provider
    with (
        patch.object(
            provider,
            "get_last_sync_time",
            MagicMock(return_value=None),
        ) as mock_get_last_sync_time,
        patch.object(
            get_films_last_sync_time_query,
            get_films_last_sync_time_query.execute.__name__,
            spy_decorator(get_films_last_sync_time_query.execute),
        ) as mock_execute,
    ):
        get_films_last_sync_time_query.execute()
    mock_get_last_sync_time.assert_called_once()
    mock_execute.mock.assert_called_once()
