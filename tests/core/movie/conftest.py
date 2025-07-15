import logging

from elasticsearch import Elasticsearch
from redis import Redis
from unittest.mock import MagicMock

from sqlalchemy.orm import Session
import pytest
from app.core.domain.movie.query import (
    GetFilmsFromPostgresQuery,
    GetFilmsLastSyncTimeQuery,
)
from app.core.domain.movie.command import (
    SaveMovieToStorageCommand,
    SetMovieLastSyncTimeCommand,
    PushMovieToQueueCommand,
)
from app.core.storage.rdb_impl import MovieLastSyncTimeProvider
from app.internal.types import LastSyncTimeProvider
from app.core.storage.rdb_impl import RedisQueue
from app.core.storage.abc import Storage
from app.core.storage.rdb_impl import RedisStorage
from app.core.domain.movie.command import SendMovieToElasticSearchCommand


@pytest.fixture
def redis() -> MagicMock:
    return MagicMock()


@pytest.fixture
def queue(logger: logging.Logger, redis: Redis) -> RedisQueue:
    return RedisQueue(log=logger, redis=redis)


@pytest.fixture
def storage(
    redis: MagicMock,
) -> Storage:
    return RedisStorage(redis=redis)


@pytest.fixture
def last_sync_time_provider(
    redis: MagicMock,
) -> LastSyncTimeProvider:
    return MovieLastSyncTimeProvider(
        redis=redis,
    )


@pytest.fixture
def save_movie_command(
    logger: MagicMock, storage: MagicMock
) -> SaveMovieToStorageCommand:
    return SaveMovieToStorageCommand(
        storage=storage,
        log=logger,
    )


@pytest.fixture
def set_movie_last_sync_time_command(
    last_sync_time_provider: LastSyncTimeProvider,
) -> SetMovieLastSyncTimeCommand:
    return SetMovieLastSyncTimeCommand(
        last_sync_time_provider=last_sync_time_provider,
    )


@pytest.fixture
def push_movie_to_queue_command(
    queue: MagicMock,
) -> PushMovieToQueueCommand:
    return PushMovieToQueueCommand(
        queue=queue,
    )


@pytest.fixture
def elastic_client() -> Elasticsearch:
    return MagicMock()


@pytest.fixture
def send_movie_to_elastic_search_command(
    logger: MagicMock,
    elastic_client: MagicMock,
) -> SendMovieToElasticSearchCommand:
    return SendMovieToElasticSearchCommand(
        log=logger,
        client=elastic_client,
    )


@pytest.fixture
def get_films_from_postgres_query(
    session: Session,
    logger: MagicMock,
) -> GetFilmsFromPostgresQuery:
    return GetFilmsFromPostgresQuery(
        log=logger,
        session=session,
    )


@pytest.fixture
def get_films_last_sync_time_query(
    last_sync_time_provider: LastSyncTimeProvider,
) -> GetFilmsLastSyncTimeQuery:
    return GetFilmsLastSyncTimeQuery(last_sync_time_provider=last_sync_time_provider)
