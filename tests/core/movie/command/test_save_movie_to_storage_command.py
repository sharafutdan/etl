from app.core.domain.movie.command import (
    SaveMovieToStorageCommand,
)
from tests.factory.movie import MovieDTOFactory
from unittest.mock import patch, ANY

from tests.tools import spy_decorator


def test_save_movie_to_storage_command(
    save_movie_command: SaveMovieToStorageCommand,
) -> None:
    movie = MovieDTOFactory.build()
    with patch.object(
        SaveMovieToStorageCommand,
        SaveMovieToStorageCommand.process.__name__,
        spy_decorator(SaveMovieToStorageCommand.process),
    ) as m:
        save_movie_command.process(value=movie)
    m.mock.assert_called_once_with(ANY, value=movie)
