import datetime

from app.core.domain.movie.command import SetMovieLastSyncTimeCommand
from unittest.mock import patch, ANY

from app.core.storage.rdb_impl import MovieLastSyncTimeProvider
from tests.tools import spy_decorator


def test_set_last_sync_time_command(
    set_movie_last_sync_time_command: SetMovieLastSyncTimeCommand,
) -> None:
    with patch.object(
        MovieLastSyncTimeProvider,
        MovieLastSyncTimeProvider.set_last_sync_time.__name__,
        spy_decorator(MovieLastSyncTimeProvider.set_last_sync_time),
    ) as m:
        value = datetime.datetime.now()
        set_movie_last_sync_time_command.process(
            value=value,
        )
    m.mock.assert_called_once_with(ANY, value)
