from unittest.mock import patch, ANY
from app.core.domain.movie.command import PushMovieToQueueCommand
from app.core.storage.rdb_impl import RedisQueue
from tests.factory.movie import MovieDTOFactory
from tests.tools import spy_decorator


def test_push_movie_to_queue_command(
    push_movie_to_queue_command: PushMovieToQueueCommand,
) -> None:
    with patch.object(
        RedisQueue, RedisQueue.push.__name__, spy_decorator(RedisQueue.push)
    ) as m:
        dto = MovieDTOFactory.build()
        push_movie_to_queue_command.process(value=dto)
    m.mock.assert_called_once_with(ANY, key=dto.key)
