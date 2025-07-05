import time
from datetime import datetime, timezone
import click
from redis import Redis

from app.core.domain.movie.command import (
    SaveMovieToStorageCommand,
    SetMovieLastSyncTimeCommand,
    PushMovieToQueueCommand,
)
from app.core.domain.movie.query import (
    GetFilmsLastSyncTimeQuery,
    GetFilmsFromPostgresQuery,
)
from app.core.storage.rdb_impl import (
    RedisStorage,
    MovieLastSyncTimeProvider,
    RedisQueue,
)
from app.telemetry.logger import logger
from app.storages.pg.base import Session
from app.storages.rdb.settings import settings as rdb_settings


@click.command()
def main() -> None:
    last_sync_time_provider = MovieLastSyncTimeProvider(
        redis=Redis.from_url(rdb_settings.url),
    )

    get_last_sync_time_query: GetFilmsLastSyncTimeQuery = GetFilmsLastSyncTimeQuery(
        last_sync_time_provider=last_sync_time_provider
    )
    set_last_sync_time_command: SetMovieLastSyncTimeCommand = (
        SetMovieLastSyncTimeCommand(last_sync_time_provider=last_sync_time_provider)
    )

    save_movie_command: SaveMovieToStorageCommand = SaveMovieToStorageCommand(
        storage=RedisStorage(redis=Redis.from_url(rdb_settings.url))
    )
    push_movie_to_queue_command: PushMovieToQueueCommand = PushMovieToQueueCommand(
        RedisQueue(
            redis=Redis.from_url(rdb_settings.url),
        )
    )

    while True:
        logger.info("Started retrieving data")
        last_sync_at = get_last_sync_time_query.execute()
        if not last_sync_at:
            last_sync_at = datetime.min

        with Session() as session:
            get_movies_query: GetFilmsFromPostgresQuery = GetFilmsFromPostgresQuery(
                session=session
            )
            movies = get_movies_query.execute(value=last_sync_at)
        for movie in movies:
            save_movie_command.process(value=movie)
            push_movie_to_queue_command.process(value=movie)

        set_last_sync_time_command.process(value=datetime.now(tz=timezone.utc))
        time.sleep(5)


if __name__ == "__main__":
    main()
