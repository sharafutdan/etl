from app.core.domain.movie.command import SendMovieToElasticSearchCommand
from unittest.mock import patch

from tests.factory.movie import MovieDTOFactory
from tests.tools import spy_decorator


def test_send_movies_to_elastic_command_bulk_called_once(
    send_movie_to_elastic_search_command: SendMovieToElasticSearchCommand,
) -> None:
    with patch.object(
        send_movie_to_elastic_search_command,
        "_bulk",
        spy_decorator(send_movie_to_elastic_search_command._bulk),
    ) as m:
        movies = MovieDTOFactory.batch(size=10)
        send_movie_to_elastic_search_command.process(
            value=iter(movies),
        )
        assert m.mock.call_count == 1


def test_send_movies_to_elastic_command_bulk_called_with_all_movies(
    send_movie_to_elastic_search_command: SendMovieToElasticSearchCommand,
) -> None:
    with patch.object(
        send_movie_to_elastic_search_command,
        "_bulk",
        spy_decorator(send_movie_to_elastic_search_command._bulk),
    ) as m:
        movies = MovieDTOFactory.batch(size=10)
        send_movie_to_elastic_search_command.process(
            value=iter(movies),
        )
        _, kwargs = m.mock.call_args
        assert len(kwargs["actions"]) == 10
